import json
import uuid
import shutil
import pandas
import tempfile
import subprocess
import contextlib

from Bio import SeqIO
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Annotated, Optional

from .core.config import settings
from .core.celery import celery_app
from .core.db import get_session_collection_pymongo

from .schemas import (
    Session,
    FileFormat,
    FileType,
    SessionFile,
    Sequence,
    Selections,
    FileConfig,
)
from .schemas import (
    AnnotationRingSchema,
    LabelRingSchema,
    BlastRingSchema,
    ReferenceRingSchema,
    GenomadRingSchema,
)
from ..rings import BlastRing, AnnotationRing, LabelRing, ReferenceRing, GenomadRing
from ..rings import Ring, RingSegment, RingType, RingReference, LabelSegment

from ..utils import slice_fasta_sequences


# Uploaded file validation and session file storage
@celery_app.task
def process_file(
    file_path: str,
    file_config: Annotated[dict, "Model dump of FileConfig"],
    filename_original: str,
):

    try:
        file = Path(file_path)
        config = FileConfig(**file_config)

        records = 0
        total_length = 0
        selections = Selections()

        if config.file_format == FileFormat.FASTA and (
            config.file_type == FileType.GENOME
            or config.file_type == FileType.REFERENCE
        ):
            total_length, records, selections = validate_fasta(path=file)
        elif (
            config.file_format == FileFormat.GENBANK
            and config.file_type == FileType.ANNOTATION_GENBANK
        ):
            records, selections = validate_genbank(path=file)
        elif (
            config.file_format == FileFormat.TSV
            and config.file_type == FileType.ANNOTATION_CUSTOM
        ):
            records = validate_tsv(path=file, file_type=config.file_type)
        elif (
            config.file_format == FileFormat.JSON
            and config.file_type == FileType.SESSION
        ):
            raise ValueError("Session file schema not allowed for this function")
        else:
            raise ValueError(
                "Could not determine file format and file type combination for processing"
            )

        session_file = SessionFile(
            session_id=config.session_id,
            id=file.name,
            name_original=filename_original,
            type=config.file_type,
            format=config.file_format,
            records=records,
            total_length=total_length,
            selections=selections,
        )

        update_files_or_create_session(session_file=session_file)

        return {"success": True, "result": session_file.model_dump()}

    except Exception as e:
        Path(file_path).unlink()  # delete for disk space
        return {"success": False, "error": str(e)}


# Uploaded file validation and session file storage
@celery_app.task
def rehydrate_session(
    file_path: str,
    file_config: Annotated[dict, "Model dump of FileConfig for JSON session file"],
):

    try:
        file = Path(file_path)
        config = FileConfig(**file_config)

        with file.open("r") as session_file:
            data = json.load(session_file)

        session = Session(**data)

        # Check if files still exist on disk and copy everything to new
        # session directory if they do, otherwise let user know the files
        # have expired and do not exist anymore

        old_session_id = session.id
        new_session_id = config.session_id

        old_session_directory = settings.WORK_DIRECTORY / old_session_id
        new_session_directory = settings.WORK_DIRECTORY / new_session_id

        if (
            old_session_directory.exists()
            and old_session_directory != new_session_directory
        ):
            # Session data and files have not expired, and the rehydration is not running on
            # the same session as before, here we copy the data over into a new directory
            # and delete the old one:
            shutil.copytree(
                old_session_directory, new_session_directory, dirs_exist_ok=True
            )
            shutil.rmtree(old_session_directory)

        # Replace session identifiers
        session_update = session.replace_session_id(new_session_id=new_session_id)

        # Add a re-hydration tag to the original filename to set expectation that
        # any operation on the file may fail (in frontend)
        session_update = session_update.add_rehydration_tag()

        # Assign a new date to session
        session_update.date = datetime.now().isoformat()

        # Update session in database
        update_session_or_create_session(session_update=session_update)

        return {"success": True, "result": session_update.model_dump()}

    except Exception as e:
        Path(file_path).unlink()  # delete for disk space
        return {"success": False, "error": str(e)}


# Reference ring, is simple but fits the format for the application


@celery_app.task
def process_reference_ring(
    reference_ring_schema: Annotated[dict, "Model dump of ReferenceRingSchema"]
):

    try:
        ring_schema = ReferenceRingSchema(**reference_ring_schema)

        ring: ReferenceRing = ReferenceRing.from_reference(
            reference=ring_schema.reference
        )

        # Ring index is modified for database in this function
        ring = update_rings_or_create_session(
            session_id=ring_schema.reference.session_id, ring=ring
        )

        return {"success": True, "result": ring.model_dump()}

    except Exception as e:
        return {"success": False, "error": str(e)}


# Nucleotide BLAST subprocess execution and parsing


@celery_app.task
def process_blast_ring(
    reference_file_path: Annotated[
        str, "Path to reference file in the session directory"
    ],
    genome_file_path: Annotated[str, "Path to genome file in the session directory"],
    blast_ring_schema: Annotated[dict, "Model dump of BlastRingSchema"],
):

    try:
        ring_schema = BlastRingSchema(**blast_ring_schema)

        with create_tmp_directory(
            root_dir=settings.WORK_DIRECTORY
        ) as working_directory:

            try:
                output_file = run_blast(
                    query_fasta=Path(genome_file_path),
                    reference_fasta=Path(reference_file_path),
                    working_directory=working_directory,
                )
            except:  # fails with generic message from subcommand exception even during timeout
                shutil.rmtree(working_directory)
                raise

            ring: BlastRing = BlastRing.from_blast_output(
                file=output_file,
                reference=ring_schema.reference,
                min_identity=ring_schema.min_identity,
                min_alignment=ring_schema.min_alignment,
                min_evalue=ring_schema.min_evalue,
            )

        if not ring.data:
            raise ValueError("BLAST executed correctly but no alignments were found")

        # Ring index is modified for database in this function
        ring = update_rings_or_create_session(
            session_id=ring_schema.reference.session_id, ring=ring
        )

        return {"success": True, "result": ring.model_dump()}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Genbank/TSV annotation extraction


@celery_app.task
def process_annotation_ring(
    genbank_file_path: Optional[
        Annotated[str, "Path to reference file in the session directory"]
    ],
    tsv_file_path: Optional[
        Annotated[str, "Path to genome file in the session directory"]
    ],
    annotation_ring_schema: Annotated[dict, "Model dump of AnnotationRingSchema"],
):

    try:
        ring_schema = AnnotationRingSchema(**annotation_ring_schema)

        if genbank_file_path:
            ring: AnnotationRing = AnnotationRing.from_genbank_file(
                file=Path(genbank_file_path),
                features=ring_schema.genbank_features,
                reference=ring_schema.reference,
                sanitize=True,
            )
        elif tsv_file_path:
            ring: AnnotationRing = AnnotationRing.from_tsv_file(
                file=Path(tsv_file_path), reference=ring_schema.reference, sanitize=True
            )
        else:
            raise ValueError("Something went wrong - no files provided")

        # Ring index is modified for database in this function
        ring = update_rings_or_create_session(
            session_id=ring_schema.reference.session_id, ring=ring
        )

        return {"success": True, "result": ring.model_dump()}

    except Exception as e:
        return {"success": False, "error": str(e)}


# Label annotations


@celery_app.task
def process_label_ring(
    tsv_file_path: Optional[
        Annotated[str, "Path to genome file in the session directory"]
    ],
    label_ring_schema: Annotated[dict, "Model dump of LabelRingSchema"],
):

    try:
        ring_schema: LabelRingSchema = LabelRingSchema(**label_ring_schema)

        # For label rings we first check if one already exists matching the same
        # reference and sequence identifiers. If so, add the ring segments to the
        # existing ring in the database and return the updated ring, otherwise
        # use the new one and insert:

        if tsv_file_path:
            ring: LabelRing = LabelRing.from_tsv_file(
                file=Path(tsv_file_path),
                reference=ring_schema.reference,
                sanitize=True,
            )
        else:
            ring: LabelRing = LabelRing(
                id=str(uuid.uuid4()), reference=ring_schema.reference
            )

        if ring_schema.labels:
            ring.add_custom_labels(
                labels=[
                    LabelSegment(
                        start=ring_segment.start,
                        end=ring_segment.end,
                        text=ring_segment.text,
                        labelIdentifier=str(uuid.uuid4()),
                    )
                    for ring_segment in ring_schema.labels
                ],
                sanitize=True,
            )

        result = check_or_update_label_ring(
            reference=ring_schema.reference, new_segments=ring.data
        )

        if result is None:
            update_rings_or_create_session(
                session_id=ring_schema.reference.session_id, ring=ring
            )
        else:
            ring = result.model_copy()

        return {"success": True, "result": ring.model_dump()}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Genomad computation


@celery_app.task
def process_genomad_ring(
    reference_file_path: Annotated[
        str, "Path to reference file in the session directory"
    ],
    genomad_ring_schema: Annotated[dict, "Model dump of GenomadRingSchema"],
):

    try:
        ring_schema = GenomadRingSchema(**genomad_ring_schema)

        storage_path = (
            settings.WORK_DIRECTORY / ring_schema.reference.session_id / "storage"
        )
        storage_file = (
            storage_path
            / f"{ring_schema.reference.reference_id}__{ring_schema.reference.sequence.id}__{ring_schema.window_size}__{ring_schema.min_window_score}.tsv"
        )

        with create_tmp_directory(
            root_dir=settings.WORK_DIRECTORY
        ) as working_directory:

            # Check if we have stored the output data already for this reference sequence

            if storage_file.exists():
                output_file = storage_file
            else:
                try:
                    output_file = run_genomad(
                        fasta=Path(reference_file_path),
                        seq_id=ring_schema.reference.sequence.id,
                        window_size=ring_schema.window_size,
                        working_directory=working_directory,
                    )
                except:  # fails with generic message from subcommand exception even during timeout
                    shutil.rmtree(working_directory)
                    raise

                storage_path.mkdir(exist_ok=True)
                shutil.copy(str(output_file), str(storage_file))

            if ring_schema.ring_type == RingType.LABEL:
                ring: LabelRing = LabelRing.from_genomad_output(
                    file=output_file,
                    reference=ring_schema.reference,
                    min_window_score=ring_schema.min_window_score,
                    min_segment_score=ring_schema.min_segment_score,
                    min_segment_length=ring_schema.min_segment_length,
                    prediction_classes=ring_schema.prediction_classes,
                )
            elif ring_schema.ring_type == RingType.ANNOTATION:
                ring: AnnotationRing = AnnotationRing.from_genomad_output(
                    file=output_file,
                    reference=ring_schema.reference,
                    min_window_score=ring_schema.min_window_score,
                    min_segment_score=ring_schema.min_segment_score,
                    min_segment_length=ring_schema.min_segment_length,
                    prediction_classes=ring_schema.prediction_classes,
                )
            else:
                ring: GenomadRing = GenomadRing.from_genomad_output(
                    file=output_file,
                    reference=ring_schema.reference,
                    min_window_score=ring_schema.min_window_score,
                )

        if not ring.data:
            raise ValueError("geNomad executed correctly but no outputs were found")

        # Ring index is modified for database in this function
        ring = update_rings_or_create_session(
            session_id=ring_schema.reference.session_id, ring=ring
        )

        return {"success": True, "result": ring.model_dump()}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Subprocess helpers


def run_genomad(
    fasta: Path, seq_id: str, window_size: int, working_directory: Path
) -> Path:
    """Slices the reference into non overlapping sequences (window_size) and runs geNomad"""

    # Database is downloaded as part of the Docker build stage in Dockerfile.server

    if not fasta.exists():
        raise FileNotFoundError(f"Reference file not found: {fasta}")

    sliced_fasta = working_directory / "sliced.fasta"

    seq_slices = slice_fasta_sequences(
        fasta_file=fasta,
        slice_size=window_size,
        sequence_subset=[seq_id],
        name_split="__",
        range_split="..",
        outfile=sliced_fasta,
    )

    if not seq_slices:
        raise ValueError("No sequence slices produced")

    base_command = [
        "genomad",
        "end-to-end",
        "--threads",
        str(settings.CELERY_THREADS_PER_PROCESS),
        "--cleanup",
        "--relaxed",
    ]
    if settings.GENOMAD_SPLITS_ARG is not None:
        base_command += [
            "--splits",
            f"{settings.GENOMAD_SPLITS_ARG}",
        ]
    base_command += [
        str(sliced_fasta),
        str(working_directory / "genomad_output"),
        str(settings.GENOMAD_DATABASE),
    ]

    try:
        subprocess.run(base_command, check=True)
    except:
        raise ValueError(
            "Failed to run `genomad` command on worker"
        )  # exception prevents command leakage on resource failure

    # Check that the output exists
    aggregated_output = (
        working_directory
        / "genomad_output"
        / "sliced_aggregated_classification"
        / "sliced_aggregated_classification.tsv"
    )
    if not aggregated_output.exists() or not aggregated_output.is_file():
        raise ValueError("Could not find geNomad aggegated output file")

    return aggregated_output


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
    try:
        subprocess.run(
            [
                "makeblastdb",
                "-in",
                str(reference_fasta),
                "-dbtype",
                "nucl",
                "-out",
                str(db_file),
            ],
            check=True,
        )
    except:
        raise ValueError(
            "Failed to run `makeblastdb` command on worker"
        )  # exception prevents command leakage on resource failure

    # Run BLASTn
    try:
        subprocess.run(
            [
                "blastn",
                "-num_threads",
                str(settings.CELERY_THREADS_PER_PROCESS),
                "-query",
                str(query_fasta),
                "-db",
                str(db_file),
                "-out",
                str(output_file),
                "-outfmt",
                "6",
            ],
            check=True,
        )
    except:
        raise ValueError(
            "Failed to run `blastn` command on worker"
        )  # exception prevents command leakage on resource failure

    if not output_file.exists() and not output_file.is_file():
        raise ValueError("Could not find BLAST output file")

    return output_file


# Validation helpers


def validate_fasta(path: Path) -> Tuple[int, int, Selections]:

    records = [r for r in SeqIO.parse(str(path), "fasta")]
    num_records = len(records)

    for record in records:
        if not validate_sequence(str(record.seq)):
            raise ValueError(
                f"Sequence {record.id} contains invalid nucleotides (IUPAC ambiguous allowed)"
            )

    if num_records < 1:
        raise ValueError("Sequence files cannot be empty")

    total_length = sum([len(r.seq) for r in records])

    return (
        total_length,
        num_records,
        Selections(sequences=[Sequence(id=r.id, length=len(r.seq)) for r in records]),
    )


def validate_genbank(path: Path) -> Tuple[int, Selections]:

    if not validate_genbank_file(file_path=path):
        raise ValueError("Invalid Genbank file format")

    records = [r for r in SeqIO.parse(str(path), "gb")]
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
        features=list(unique_features),
    )


def validate_tsv(path: Path, file_type: FileType) -> int:

    data = pandas.read_csv(path, sep="\t", header=0)

    if file_type == FileType.ANNOTATION_CUSTOM and len(data.columns) != 3:
        raise ValueError(
            "Custom annotation files must have three columns (start, end, text)"
        )

    for c in ("start", "end", "text"):
        if c not in data.columns:
            raise ValueError(
                f"Custom annotation files must have a column with header {c}"
            )

    for i, row in data.iterrows():
        if row["start"] > row["end"]:
            raise ValueError(
                f"Start values cannot be greater than end values (row {i})"
            )

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

    with file_path.open("r") as file:
        first_line = file.readline().strip()
        if not first_line.startswith("LOCUS"):
            return False  # GenBank file should start with 'LOCUS'

        # Read the file until the end to find the terminating "//"
        for line in file:
            if line.strip() == "//":
                return True  # Found the terminating line

        return False  # Terminating "//" line not found


# Database helpers (workers are not async)

# No further error handling as any errors here will bubble
# up to the general exception handling in the task


def update_files_or_create_session(session_file: SessionFile) -> str:

    sessions_collection = get_session_collection_pymongo()

    # Check if session exists and update or create
    session = sessions_collection.find_one({"id": session_file.session_id})

    if session:
        sessions_collection.update_one(
            {"id": session_file.session_id},
            {"$push": {"files": session_file.model_dump()}},
        )
    else:
        new_session = Session(
            id=session_file.session_id,
            date=datetime.now().isoformat(),
            files=[session_file],
            rings=[],
        )
        sessions_collection.insert_one(new_session.model_dump())

    return session_file.session_id


def update_rings_or_create_session(session_id: str, ring: Ring) -> str:

    sessions_collection = get_session_collection_pymongo()

    # Check if session exists and update or create
    session = sessions_collection.find_one({"id": session_id})

    if session:
        session_model = Session(**session)

        # Filter rings with the same reference sequence
        same_ref_rings = [
            r
            for r in session_model.rings
            if r.reference.reference_id == ring.reference.reference_id
            and r.reference.sequence.id == ring.reference.sequence.id
        ]

        # Sort these rings by their index
        same_ref_rings.sort(key=lambda r: r.index)

        # Check if a RingType.LABEL ring with the same reference exists
        label_ring = next((r for r in same_ref_rings if r.type == RingType.LABEL), None)

        # Assign the index for the new Ring
        if label_ring and ring.type != RingType.LABEL:
            # Set to the second-last position
            ring.index = len(same_ref_rings) - 1
            # Move the label ring to the last index if it's not already
            if label_ring.index != len(same_ref_rings):
                label_ring.index = len(same_ref_rings)
        else:
            # Otherwise, assign the last index
            ring.index = len(same_ref_rings)

        # Add the new ring to the session rings
        session_model.rings.append(ring)

        # Update the session in the database
        sessions_collection.update_one(
            {"id": session_id},
            {"$set": {"rings": [r.model_dump() for r in session_model.rings]}},
        )
    else:
        new_session = Session(
            id=session_id, date=datetime.now().isoformat(), files=[], rings=[ring]
        )
        sessions_collection.insert_one(new_session.model_dump())

    # Return ring because we modify its index and the
    # ring itself is returned in response
    return ring


def update_session_or_create_session(session_update: Session):

    sessions_collection = get_session_collection_pymongo()

    # Check if session exists and update or create
    session = sessions_collection.find_one({"id": session_update.id})

    if session:
        sessions_collection.update_one(
            {"id": session_update.id}, {"$set": session_update.model_dump()}
        )
    else:
        sessions_collection.insert_one(session_update.model_dump())

    return session_update.id  # new id


def check_or_update_label_ring(
    reference: RingReference, new_segments: List[RingSegment]
) -> LabelRing | None:

    sessions_collection = get_session_collection_pymongo()

    result = sessions_collection.find_one(
        {
            "id": reference.session_id,
            "rings": {
                "$elemMatch": {
                    "type": RingType.LABEL,
                    "reference.reference_id": reference.reference_id,
                    "reference.sequence.id": reference.sequence.id,
                }
            },
        }
    )

    if result:

        ring_id = None
        for ring in result.get("rings", []):
            if (
                ring.get("type") == RingType.LABEL
                and ring.get("reference", {}).get("reference_id")
                == reference.reference_id
                and ring.get("reference", {}).get("sequence", {}).get("id")
                == reference.sequence.id
            ):
                ring_id = ring.get("id")
                break

        if ring_id is not None:

            # Update the ring with new ring segments
            update_result = sessions_collection.update_one(
                {"id": reference.session_id, "rings.id": ring_id},
                {
                    "$push": {
                        "rings.$.data": {
                            "$each": [segment.model_dump() for segment in new_segments]
                        }
                    }
                },
            )

            if update_result.modified_count > 0:
                # Retrieve and return the updated ring
                updated_session = sessions_collection.find_one(
                    {"id": reference.session_id}
                )
                updated_ring = next(
                    (
                        ring
                        for ring in updated_session["rings"]
                        if ring["id"] == ring_id
                    ),
                    None,
                )
                return LabelRing(**updated_ring)
            else:
                return None
        else:
            return None
    else:
        return None


# Working directory helpers


@contextlib.contextmanager
def create_tmp_directory(root_dir: str = None) -> Path:
    with tempfile.TemporaryDirectory(dir=root_dir) as temp_dir:
        yield Path(temp_dir)
