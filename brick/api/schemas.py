from pydantic import BaseModel
from typing import Optional
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

class TaskStatus(StrEnum):
    PENDING = 'PENDING' 
    STARTED = 'STARTED'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    PROCESSING = 'PROCESSING'


class FileConfig(BaseModel):
    session_id: str
    file_format: FileFormat
    file_type: FileType


class SessionFile(BaseModel):
    session_id: str
    id: str             # without ext
    name: str           # with ext
    name_original: str  
    type: str
    format: str
    records: int 
    length: int 


class UploadFileResponse(BaseModel):
    task_id: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: TaskStatus


class TaskResultResponse(TaskStatusResponse):
    result: Optional[SessionFile]