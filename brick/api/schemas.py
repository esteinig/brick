from pydantic import BaseModel
from enum import StrEnum

class FileFormat(StrEnum):
    FASTA = 'fasta'
    GENBANK = 'genbank'
    TSV = 'tsv'

class FileType(StrEnum):
    REFERENCE = 'reference'
    GENOME = 'genome'
    ANNOTATION_GENBANK = 'annotation_genbank'
    ANNOTATION_CUSTOM = 'annotation_custom'

class FileConfig(BaseModel):
    session_id: str
    file_format: FileFormat
    file_type: FileType
