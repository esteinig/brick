from pydantic import BaseModel, validator
from typing import Optional, Annotated, Tuple, List, Union
from pathlib import Path
from enum import StrEnum
from uuid import UUID

from .core.config import settings
from ..rings import BlastRing, AnnotationRing

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


class Selections(BaseModel):
    sequences: List[str] = []
    qualifiers: List[str] = []
    features: List[str] = []


class SessionFile(BaseModel):
    session_id: SessionFileID
    id: SessionFileID             # uuid - filename in session directory
    type: FileType
    format: FileFormat
    records: int 
    length: int 
    name_original: str  
    selections: Selections


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
    result: Optional[SessionFile | BlastRing | AnnotationRing]


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


# Annotation ring
    

class AnnotationRingSchema(BaseModel):
    session_id: SessionID
    genbank_id: SessionFileID | None
    tsv_id: SessionFileID | None
    genbank_features: List[str]
    genbank_qualifiers: List[str]

    @validator('genbank_id', pre=True)
    def check_fields(cls, v, values):
        tsv_id = values.get('tsv_id')
        if tsv_id is None and v is None:
            ValueError("One of 'genbank_id' or 'tsv_id' fields must be provided")
        return v
    
    @validator('session_id', 'genbank_id', 'tsv_id')
    def check_uuid_v4(cls, v):
        if v is not None:
            try:
                UUID(v, version=4)
            except ValueError:
                raise ValueError(f"Value '{v}' is not a valid UUID version 4")
        return v
    
    @validator('session_id')
    def check_session_directory(cls, v):
        assert (settings.WORK_DIRECTORY / v).exists(), f"Session directory '{v}' does not exist"
        return v

    
    @validator('genbank_id', 'tsv_id')
    def check_input_files(cls, v, values):
        session_id = values.get('session_id')
        if v is not None:
            assert (settings.WORK_DIRECTORY / session_id / v).exists(), f"Input file '{v}' does not exist"
        return v
    
    
    def get_file_paths(self) -> Tuple[Path, Path | None, Path | None]:

        return (
            settings.WORK_DIRECTORY / self.session_id, 
            settings.WORK_DIRECTORY / self.session_id / self.genbank_id if self.genbank_id else None, 
            settings.WORK_DIRECTORY / self.session_id / self.tsv_id  if self.tsv_id else None
        )

class AnnotationRingResponse(BaseModel):
    task_id: CeleryTaskID