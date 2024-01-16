import pandas
import subprocess
import tempfile
import contextlib

from Bio import SeqIO
from typing import Tuple, Annotated, Optional
from pathlib import Path
from datetime import datetime

from .core.config import settings
from .core.celery import celery_app
from .core.db import get_session_collection_pymongo
from .schemas import FileFormat, FileType, SessionFile, Selections, FileConfig, AnnotationRingSchema, LabelRingSchema, Sequence, BlastRingSchema
from .models import Session
from ..rings import BlastRing, AnnotationRing, LabelRing

# Uploaded file validation and session file storage
@celery_app.task
def process_file(file_path: str, file_config: Annotated[dict, "Model dump of FileConfig"], filename_original: str):

    try:
        file = Path(file_path)
        config = FileConfig(**file_config)

        records = 0; total_length = 0; selections = Selections()

        if config.file_format == FileFormat.FASTA:
            total_length, records, selections = validate_fasta(path=file)
        elif config.file_format == FileFormat.GENBANK:
            records, selections = validate_genbank(path=file)
        elif config.file_format == FileFormat.TSV:
            records = validate_tsv(path=file, file_type=config.file_type)

        session_file = SessionFile(
            session_id=config.session_id,
            id=file.name,
            name_original=filename_original,
            type=config.file_type,
            format=config.file_format,
            records=records,
            total_length=total_length,
            selections=selections
        )

        update_or_create_session(session_file=session_file)

        return {
            "success": True, 
            "result": session_file.model_dump()
        }

    except Exception as e:
        Path(file_path).unlink() # delete for disk space
        return {"success": False, "error": str(e)}
    


# Nucleotide BLAST subprocess execution and parsing
    
@celery_app.task
def process_blast_ring(
    reference_file_path: Annotated[str, "Path to reference file in the session directory"], 
    genome_file_path: Annotated[str, "Path to genome file in the session directory"], 
    blast_ring_schema: Annotated[dict, "Model dump of BlastRingSchema"]
):

    try:
        ring_schema = BlastRingSchema(**blast_ring_schema)

        with create_tmp_directory(root_dir=settings.WORK_DIRECTORY) as working_directory:
            output_file = run_blast(
                query_fasta=Path(genome_file_path), 
                reference_fasta=Path(reference_file_path), 
                working_directory=working_directory
            )
            ring: BlastRing = BlastRing.from_blast_output(
                file=output_file, reference=ring_schema.reference
            )

             
        return {
            "success": True, 
            "result": ring.model_dump()
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

# Genbank/TSV annotation extraction
    
@celery_app.task
def process_annotation_ring(
    genbank_file_path: Optional[Annotated[str, "Path to reference file in the session directory"]], 
    tsv_file_path: Optional[Annotated[str, "Path to genome file in the session directory"]], 
    annotation_ring_schema: Annotated[dict, "Model dump of AnnotationRingSchema"]
):

    try:
        ring_schema = AnnotationRingSchema(**annotation_ring_schema)

        if genbank_file_path:
            ring: AnnotationRing  = AnnotationRing.from_genbank_file(
                file=Path(genbank_file_path), 
                features=ring_schema.genbank_features,
                reference=ring_schema.reference,
                sanitize=True
            )
        elif tsv_file_path:
            ring: AnnotationRing = AnnotationRing.from_tsv_file(
                file=Path(tsv_file_path),
                reference=ring_schema.reference,
                sanitize=True
            )
        else:
            raise ValueError("Something went wrong - no files provided")

        return {
            "success": True, 
            "result": ring.model_dump()
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

@celery_app.task
def process_label_ring(
    tsv_file_path: Optional[Annotated[str, "Path to genome file in the session directory"]], 
    label_ring_schema: Annotated[dict, "Model dump of LabelRingSchema"]
):

    try:
        ring_schema = LabelRingSchema(**label_ring_schema)

        if tsv_file_path:
            ring: LabelRing = LabelRing.from_tsv_file(
                file=Path(tsv_file_path),
                reference=ring_schema.reference,
                sanitize=True
            )
        else:
            ring: LabelRing = LabelRing(
                reference=ring_schema.reference
            )

        if ring_schema.labels:
            ring.add_custom_labels(
                labels=ring_schema.labels, 
                sanitize=True
            )

        return {
            "success": True, 
            "result": ring.model_dump()
        }

    except Exception as e:
        return {"success": False, "error": str(e)}



# Subprocess helpers
    

def run_blast(query_fasta: Path, reference_fasta: Path, working_directory: Path):
    """
    Runs a nucleotide BLAST comparing a query genome in FASTA format with a reference genome.

    :param query_fasta: Path to the query genome FASTA file.
    :param reference_fasta: Path to the reference genome FASTA file.
    :param output_file: Path to save the BLAST results.
    """

    # Check if files exist
    if not query_fasta.exists():
        raise FileNotFoundError(f"Query file not found: {query_fasta}")
    if not reference_fasta.exists():
        raise FileNotFoundError(f"Reference file not found: {reference_fasta}")

    db_file = working_directory / "refdb"
    output_file = working_directory / "results.tsv"

    # Create BLAST database from reference genome
    subprocess.run(["makeblastdb", "-in", str(reference_fasta), "-dbtype", "nucl", "-out", str(db_file)], check=True)

    # Run BLASTn
    subprocess.run(["blastn", "-query", str(query_fasta), "-db", str(db_file), "-out", str(output_file), "-outfmt", "6"], check=True)

    return output_file

# Validation helpers

def validate_fasta(path: Path) -> Tuple[int, int, Selections]:

    records = [r for r in SeqIO.parse(str(path), 'fasta')]
    num_records = len(records)

    for record in records:
        if not validate_sequence(str(record.seq)):
            raise ValueError(f"Sequence {record.id} contains invalid nucleotides (IUPAC ambiguous allowed)")

    if num_records < 1:
        raise ValueError("Sequence files cannot be empty")
    
    total_length = sum([len(r.seq) for r in records])

    return total_length, num_records, Selections(
        sequences=[Sequence(id=r.id, length=len(r.seq)) for r in records]
    )


def validate_genbank(path: Path) -> Tuple[int, Selections]:

    if not validate_genbank_file(file_path=path):
        raise ValueError("Invalid Genbank file format")
    
    records = [r for r in SeqIO.parse(str(path), 'gb')]
    num_records = len(records)

    if num_records < 1:
        raise ValueError("Genbank files cannot be empty")
    

    unique_features = set()
    unique_qualifiers = set()

    for record in records:
        for feature in record.features:
            unique_features.add(feature.type)
            for key in feature.qualifiers.keys():
                unique_qualifiers.add(key)
    
    return num_records, Selections(
        sequences=[Sequence(id=r.id, length=len(r.seq)) for r in records],
        qualifiers=list(unique_qualifiers),
        features=list(unique_features)
    )


def validate_tsv(path: Path, file_type: FileType) -> int:

    data = pandas.read_csv(path, sep="\t", header=0)

    if file_type == FileType.ANNOTATION_CUSTOM and len(data.columns) != 4:
        raise ValueError("Custom annotation files must have four columns (start, end, text, color)")
    if file_type == FileType.ANNOTATION_GENBANK  and data.columns != ["start", "end", "text", "color"]:
        raise ValueError("Custom annotation files must have four column headers in order (start, end, text, color)")
    
    for i, row in data.iterrows():
        if row['start'] > row['end']:
            raise ValueError(f"Start values cannot be greater than end values (row {i})")
        
    num_records = len(data)

    if num_records < 1:
        raise ValueError("Custom annotation files cannot be empty")

    return num_records

def validate_sequence(sequence: str) -> bool:
    """
    Validates the sequence data using BioPython's IUPAC ambiguous nucleotide codes.
    
    Args:
    sequence (str): Sequence data from the FASTA file.
    
    Returns:
    bool: True if the sequence data contains only valid IUPAC ambiguous nucleotide codes, False otherwise.
    """
    valid_nucleotides = set("ACGTURYSWKMBDHVN")
    return all(nucleotide in valid_nucleotides for nucleotide in sequence.upper())

def validate_genbank_file(file_path: Path):
    """
    Validates if a file is in the GenBank format.
    
    Args:
    file_path (str): Path to the GenBank file.
    
    Returns:
    bool: True if the file is in the GenBank format, False otherwise.
    """
    
    with file_path.open('r') as file:
        first_line = file.readline().strip()
        if not first_line.startswith('LOCUS'):
            return False  # GenBank file should start with 'LOCUS'
        
        # Read the file until the end to find the terminating "//"
        for line in file:
            if line.strip() == '//':
                return True  # Found the terminating line
        
        return False  # Terminating "//" line not found
    

# Database helpers (workers are not async)

# No further error handling as any errors here will bubble
# up to the general exception handling in the task

def update_or_create_session(session_file: SessionFile) -> str:

    sessions_collection = get_session_collection_pymongo()

    # Check if session exists and update or create
    session = sessions_collection.find_one({"id": session_file.session_id})

    if session:
        sessions_collection.update_one(
            {"id": session_file.session_id}, 
            {"$push": {"files": session_file.model_dump()}}
        )
    else:
        new_session = Session(
            id=session_file.session_id, 
            date=datetime.now().isoformat(), 
            files=[session_file]
        )
        sessions_collection.insert_one(
            new_session.model_dump()
        )

    return session_file.session_id


# Working directory helpers

@contextlib.contextmanager
def create_tmp_directory(root_dir: str = None) -> Path:
    with tempfile.TemporaryDirectory(dir=root_dir) as temp_dir:
        yield Path(temp_dir)