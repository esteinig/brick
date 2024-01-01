from pydantic import BaseModel, validator
from typing import Optional, Annotated, Tuple
from pathlib import Path
from enum import StrEnum
from uuid import UUID

from .core.config import settings
from ..rings import BlastRing

SessionID = Annotated[str, "Session UUID used as directory name of the session directory"]
SessionFileID = Annotated[str, "Uploaded file assigned UUID used as filename in session directory"]
CeleryTaskID =  Annotated[str, "Celery task UUID"]

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
    id: SessionFileID             # uuid - filename in session directory
    type: FileType
    format: FileFormat
    records: int 
    length: int 
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
    result: Optional[SessionFile | BlastRing] 


# Ring schemas

class BlastMethod(StrEnum):
    BLASTN = 'blastn'

class BlastRingSchema(BaseModel):
    session_id: SessionID
    reference_id: SessionFileID
    genome_id: SessionFileID
    blast_method: BlastMethod
    min_alignment: int
    min_identity: float

    @validator('session_id', 'reference_id', 'genome_id')
    def check_uuid_v4(cls, v):
        try:
            UUID(v, version=4)
        except ValueError:
            raise ValueError(f"Value '{v}' is not a valid UUID version 4")
        return v
    
    @validator('session_id')
    def check_session_directory(cls, v):
        assert (settings.WORK_DIRECTORY / v).exists(), f"Session directory '{v}' does not exist"
        return v


    @validator('reference_id', 'genome_id')
    def check_input_files(cls, v, values):
        session_id = values.get('session_id')
        assert (settings.WORK_DIRECTORY / session_id / v).exists(), f"Input file '{v}' does not exist"
        return v


    @validator('min_alignment')
    def check_min_alignment(cls, v):
        assert 0 <= v <= 100, 'Minimum alignment length must be greater or equal to 0'
        return v
    
    @validator('min_identity')
    def check_min_identity(cls, v):
        assert 0 <= v <= 100, 'Minimum identity must be between 0 and 100'
        return v
    
    def get_file_paths(self) -> Tuple[Path, Path, Path]:

        return (
            settings.WORK_DIRECTORY / self.session_id, 
            settings.WORK_DIRECTORY / self.session_id / self.reference_id, 
            settings.WORK_DIRECTORY / self.session_id / self.genome_id
        )


class BlastRingResponse(BaseModel):
    task_id: CeleryTaskID