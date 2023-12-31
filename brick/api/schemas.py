from pydantic import BaseModel
from typing import Optional, Annotated
from enum import StrEnum


SessionID = Annotated[str, "Session identifier"]
SessionFileID = Annotated[str, "SessionFile identifier"]
CeleryTaskID =  Annotated[str, "Celery task identifier"]

# File uploads

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
    session_id: SessionFileID
    file_format: FileFormat
    file_type: FileType


class SessionFile(BaseModel):
    session_id: SessionFileID
    id: SessionFileID             # uuid
    type: FileType
    format: FileFormat
    records: int 
    length: int 
    name: str                     # with ext
    name_original: str  


class UploadFileResponse(BaseModel):
    task_id: CeleryTaskID


# Celery tasks
    

class TaskStatus(StrEnum):
    PENDING = 'PENDING' 
    STARTED = 'STARTED'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    PROCESSING = 'PROCESSING'


class TaskStatusResponse(BaseModel):
    task_id: CeleryTaskID
    status: TaskStatus


class TaskResultResponse(TaskStatusResponse):
    result: Optional[SessionFile]


# Ring schemas

class BlastMethod(StrEnum):
    BLASTN = 'blastn'

class BlastRingConfig(BaseModel):
    session_id: SessionID
    reference_id: SessionFileID
    genome_id: SessionFileID
    blast_method: BlastMethod
    blast_min_alignment: int
    blast_min_identity: float

