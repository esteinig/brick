from pydantic import BaseModel, ValidationInfo, field_validator
from typing import Optional, Annotated, Tuple, List
from pathlib import Path
from enum import StrEnum
from uuid import UUID

import uuid

from .core.config import settings
from ..rings import BlastRing, AnnotationRing, LabelRing, RingSegment, RingReference

SessionID = Annotated[str, "Session UUID used as directory name of the session directory"]
SessionFileID = Annotated[str, "Uploaded file assigned UUID used as filename in session directory"]
SequenceID = Annotated[str, "Uploaded FASTA sequence ID used as selector for the ring reference"]
CeleryTaskID =  Annotated[str, "Celery task UUID"]

# Schemas inherit from this class to provide a method to create a temporary sessions directory
# for testing endpoint validators on the schema models

class RingSchema(BaseModel):
    
    reference: RingReference

    @field_validator('reference')
    def check_uuid_v4(cls, v: RingReference):
        if v is not None:
            try:
                UUID(v.session_id, version=4)
            except ValueError:
                raise ValueError(f"value '{v.session_id}' is not a valid UUID version 4")
        return v
    
    @field_validator('reference')
    def check_session_directory(cls, v: RingReference):
        if not (settings.WORK_DIRECTORY / v.session_id).exists():
            raise ValueError(f"session directory '{v}' does not exist")
        return v


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


class Sequence(BaseModel):
    id: str
    length: int

class Selections(BaseModel):
    sequences: List[Sequence] = []
    qualifiers: List[str] = []
    features: List[str] = []


class SessionFile(BaseModel):
    session_id: SessionFileID
    id: SessionFileID             # uuid - filename in session directory
    type: FileType
    format: FileFormat
    records: int 
    total_length: int 
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
    result: Optional[SessionFile | BlastRing | AnnotationRing | LabelRing]


# Ring schemas
class BlastMethod(StrEnum):
    BLASTN = 'blastn'

class BlastRingSchema(RingSchema):
    genome_id: SessionFileID
    blast_method: BlastMethod = BlastMethod.BLASTN
    min_alignment: int = 0
    min_identity: float = 0


    @field_validator('genome_id')
    def check_uuid_v4(cls, v: SessionFileID):
        try:
            UUID(v, version=4)
        except ValueError:
            raise ValueError(f"value '{v}' is not a valid UUID version 4")
        return v
    
    @field_validator('reference')
    def check_reference_id_input_file(cls, v: RingReference):
        if v is not None and not (settings.WORK_DIRECTORY / v.session_id / v.reference_id).exists():
            raise ValueError(f"reference input file '{v.reference_id}' does not exist")
        return v

    @field_validator('genome_id')
    def check_genome_id_input_file(cls, v: SessionFileID, info: ValidationInfo):
        ref: RingReference = info.data.get('reference')
        if v is not None and not (settings.WORK_DIRECTORY / ref.session_id / v).exists():
            raise ValueError(f"genome input file '{v}' does not exist")
        return v

    @field_validator('min_alignment')
    def check_min_alignment(cls, v: int):
        if not v >= 0:
            raise ValueError('minimum alignment length must be greater or equal to 0')
        return v
    
    @field_validator('min_identity')
    def check_min_identity(cls, v: int):
        if not 0 <= v <= 100:
            raise ValueError('minimum identity must be between 0 and 100')
        return v
    
    def get_file_paths(self) -> Tuple[Path, Path, Path]:

        return (
            settings.WORK_DIRECTORY / self.reference.session_id, 
            settings.WORK_DIRECTORY / self.reference.session_id / self.reference.reference_id, 
            settings.WORK_DIRECTORY / self.reference.session_id / self.genome_id
        )


class BlastRingResponse(BaseModel):
    task_id: CeleryTaskID


# Annotation ring

class AnnotationRingSchema(RingSchema):
    genbank_id: SessionFileID | None = None
    tsv_id: SessionFileID | None = None
    genbank_features: List[str] = []
    genbank_qualifiers: List[str] = []


    @field_validator('genbank_id')
    def check_fields(cls, v: SessionFileID, info: ValidationInfo):
        tsv_id = info.data.get('tsv_id')
        if tsv_id is None and v is None:
            ValueError("one of 'genbank_id' (genbank file) or 'tsv_id' (ring segment file) identifiers must be provided")
        return v
    
    @field_validator('genbank_id', 'tsv_id')
    def check_uuid_v4(cls, v: SessionFileID):
        if v is not None:
            try:
                UUID(v, version=4)
            except ValueError:
                raise ValueError(f"value '{v}' is not a valid UUID version 4")
        return v
    
    @field_validator('genbank_id', 'tsv_id')
    def check_input_files(cls, v: SessionFileID, info: ValidationInfo):
        ref: RingReference = info.data.get('reference')
        if v is not None:
            if not (settings.WORK_DIRECTORY / ref.session_id / v).exists():
                raise ValueError(f"input file '{v}' does not exist")
        return v
    
    def get_file_paths(self) -> Tuple[Path, Path | None, Path | None]:

        return (
            settings.WORK_DIRECTORY / self.reference.session_id, 
            settings.WORK_DIRECTORY / self.reference.session_id / self.genbank_id if self.genbank_id else None, 
            settings.WORK_DIRECTORY / self.reference.session_id / self.tsv_id  if self.tsv_id else None
        )

class AnnotationRingResponse(BaseModel):
    task_id: CeleryTaskID



# Label ring


class LabelRingSchema(RingSchema):
    tsv_id: SessionFileID | None  = None
    labels: List[RingSegment] = []

    @field_validator('tsv_id')
    def check_uuid_v4(cls, v: SessionFileID):
        if v is not None:
            try:
                UUID(v, version=4)
            except ValueError:
                raise ValueError(f"value '{v}' is not a valid UUID version 4")
        return v
    
    @field_validator('tsv_id')
    def check_input_files(cls, v: SessionFileID, info: ValidationInfo):
        ref: RingReference = info.data.get('reference')
        if v is not None:
            if not (settings.WORK_DIRECTORY / ref.session_id / v).exists():
                raise ValueError(f"input file '{v}' does not exist")
        return v
    
    @field_validator('labels')
    def check_labels_input(cls, v: List[RingSegment], info: ValidationInfo):
        tsv_id = info.data.get('tsv_id')
        if not v and tsv_id is None:
            raise ValueError(f"one of 'tsv_id' (file identifier) or 'labels' (list of ring segments) must be provided")
        return v
    
    def get_file_paths(self) -> Tuple[Path, Path | None]:

        return (
            settings.WORK_DIRECTORY / self.reference.session_id, 
            settings.WORK_DIRECTORY / self.reference.session_id / self.tsv_id if self.tsv_id else None
        )

class LabelRingResponse(BaseModel):
    task_id: CeleryTaskID