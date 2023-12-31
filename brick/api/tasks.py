import pandas
import subprocess

from Bio import SeqIO
from typing import Tuple
from pathlib import Path
from datetime import datetime
from uuid import uuid4

from .core.celery import celery_app
from .core.db import get_session_collection_pymongo
from .schemas import FileFormat, FileType, SessionFile
from .models import Session


# Uploaded file validation and session file storage
@celery_app.task
def process_file(file_path: str, config_data: dict, filename_original: str):

    try:
        session_id: str = config_data["session_id"]
        file_type: FileType = config_data["file_type"]
        file_format: FileFormat = config_data["file_format"]

        records = 0; length = 0

        if file_format == FileFormat.FASTA:
            length, records = validate_fasta(path=file_path, file_type=file_type)
        elif file_format == FileFormat.GENBANK:
            records = validate_genbank(path=file_path)
        elif file_format == FileFormat.TSV:
            records = validate_tsv(path=file_path, file_type=file_type)

        session_file = SessionFile(
            session_id=session_id,
            id=Path(file_path).stem,
            name=Path(file_path).name,
            name_original=filename_original,
            type=file_type,
            format=file_format,
            records=records,
            length=length
        )

        update_or_create_session(session_file=session_file)

        return {
            "success": True, 
            "result": session_file.model_dump()
        }

    except Exception as e:
        # Delete the file if processing fails
        Path(file_path).unlink()

        # Capture any exceptions and return them
        return {"success": False, "error": str(e)}
    


# Nucleotide BLAST subprocess execution and parsing
@celery_app.task
def creat_blast_ring(reference_file: str, genome_file: str, config_data: dict):

    try:
        
        output_name = run_nucleotide_blast(query_fasta=Path(genome_file), reference_fasta=Path(reference_file), output_file=Path())

        update_or_create_session(session_file=session_file)

        return {
            "success": True, 
            "result": session_file.model_dump()
        }

    except Exception as e:
        # Delete the file if processing fails
        Path(file_path).unlink()

        # Capture any exceptions and return them
        return {"success": False, "error": str(e)}



# Subprocess helpers
    

def run_nucleotide_blast(query_fasta: Path, reference_fasta: Path, output_file: Path):
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

    # Create BLAST database from reference genome
    subprocess.run(["makeblastdb", "-in", reference_fasta, "-dbtype", "nucl", "-out", db_name], check=True)

    # Run BLASTn
    subprocess.run(["blastn", "-query", query_fasta, "-db", db_name, "-out", output_file, "-outfmt 6"], check=True)


# Validation helpers

def validate_fasta(path: Path, file_type: FileType) -> Tuple[int, int]:

    seqs = [r for r in SeqIO.parse(str(path), 'fasta')]
    length = sum([len(r.seq) for r in seqs])
    records = len(seqs)

    if file_type == FileType.REFERENCE and records > 1:
        raise ValueError("Reference sequence files must consist of a single contig")
    
    return length, records


def validate_genbank(path: Path) -> int:

    records = len([r for r in SeqIO.parse(str(path), 'gb')])
    
    return records


def validate_tsv(path: Path, file_type: FileType) -> int:

    data = pandas.read_csv(path, sep="\t", header=0)

    if file_type == FileType.ANNOTATION_CUSTOM and len(data.columns) != 4:
        raise ValueError("Custom annotation files must have four columns (start, end, text, color)")
    if file_type == FileType.ANNOTATION_GENBANK  and data.columns != ["start", "end", "text", "color"]:
        raise ValueError("Custom annotation files must have four column headers in order (start, end, text, color)")
    
    records = len(data)

    return records

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