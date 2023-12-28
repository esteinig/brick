from .core.celery import celery_app
from .schemas import FileFormat, FileType
from pathlib import Path

import pandas

from pydantic import BaseModel
from pathlib import Path

from Bio import SeqIO

class ProcessFileResult(BaseModel):
    name: str
    file: str
    id: str
    path: str
    type: str
    format: str
    records: int 
    length: int 



# Celery Task
@celery_app.task
def process_file(file_path: str, config: dict, original_filename: str):

    try:
        # Perform long-running task processing on file
        # Example: read file, process data, etc.

        file_format: FileFormat = config["file_format"]
        file_type: FileType = config["file_type"]

        records = 0
        length = 0

        if file_format == FileFormat.FASTA:
            # Validating Fasta format by parsing and counting records/bases
            seqs = [r for r in SeqIO.parse(str(file_path), 'fasta')]
            length = sum([len(r.seq) for r in seqs])
            records = len(seqs)

            if file_type == FileType.REFERENCE and records > 1:
                raise ValueError("Reference genome files must have a single contig in BRICK v0.1.0")

        elif file_format == FileFormat.GENBANK:
            # Validating Genbank format by parsing and counting records
            records = len([r for r in SeqIO.parse(str(file_path), 'gb')])

        elif file_format == FileFormat.TSV:
            # Validating TSV format by parsing and checking columns
            data = pandas.read_csv(file_path, sep="\t", header=0)

            if file_type == FileType.ANNOTATION_CUSTOM and len(data.columns) != 4:
                raise ValueError("Custom annotation files must have four columns (start, end, text, color) in BRICK v0.1.0")
            if file_type == FileType.ANNOTATION_GENBANK  and data.columns != ["start", "end", "text", "color"]:
                raise ValueError("Custom annotation files must have four column headers in order (start, end, text, color) in BRICK v0.1.0")
            
            records = len(data)

        return {
            "success": True, 
            "result": ProcessFileResult(
                name=original_filename,
                file=Path(file_path).name,
                id=Path(file_path).stem,
                path=file_path,
                type=file_type,
                format=file_format,
                records=records,
                length=length
            ).dict()
        }

    except Exception as e:
        # Delete the file
        Path(file_path).unlink()
        # Capture any exceptions and return them
        return {"success": False, "error": str(e)}


        