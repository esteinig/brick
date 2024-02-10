import shutil

from pydantic import BaseModel, field_validator, model_validator
from typing import Optional, Annotated, Tuple, List
from strenum import StrEnum
from pathlib import Path
from uuid import UUID

from .core.config import settings

from ..rings import BlastRing, AnnotationRing, LabelRing, ReferenceRing, GenomadRing
from ..rings import RingSegment, RingReference, RingType, Ring
from ..rings import GenomadPredictionClass

SessionID = Annotated[
    str, "Session UUID used as directory name of the session directory"
]
SessionFileID = Annotated[
    str, "Uploaded file assigned UUID used as filename in session directory"
]
SequenceID = Annotated[
    str, "Uploaded FASTA sequence ID used as selector for the ring reference"
]
CeleryTaskID = Annotated[str, "Celery task UUID"]

# Schemas inherit from this class to provide a method to create a temporary sessions directory
# for testing endpoint validators on the schema models


class RingSchema(BaseModel):

    reference: RingReference

    @field_validator("reference")
    @classmethod
    def check_uuid_v4(cls, v: RingReference):
        try:
            UUID(v.session_id, version=4)
        except ValueError:
            raise ValueError(f"value '{v.session_id}' is not a valid UUID version 4")
        return v

    @field_validator("reference")
    @classmethod
    def check_session_directory(cls, v: RingReference):
        if not (settings.WORK_DIRECTORY / v.session_id).exists():
            raise ValueError(f"session directory '{v}' does not exist")

        return v


##############
# FILE UPLOAD
#############
class FileFormat(StrEnum):
    FASTA = "fasta"
    GENBANK = "genbank"
    TSV = "tsv"
    JSON = "json"


class FileType(StrEnum):
    REFERENCE = "reference"
    GENOME = "genome"
    ANNOTATION_GENBANK = "annotation_genbank"
    ANNOTATION_CUSTOM = "annotation_custom"
    SESSION = "session"


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
    id: SessionFileID  # uuid - filename in session directory
    type: FileType
    format: FileFormat
    records: int
    total_length: int
    name_original: str
    selections: Selections


class UploadFileResponse(BaseModel):
    task_id: CeleryTaskID


class Session(BaseModel):
    id: str
    date: str
    files: List[SessionFile]
    rings: List[Ring]

    def validate_file_paths(self):
        for file in self.files:
            file_path = settings.WORK_DIRECTORY / file.session_id / file.id
            if not file_path.exists():
                raise FileNotFoundError(
                    f"Could not find file `{file.name_original}` in session directory path: {file_path}"
                )

    def replace_session_id(self, new_session_id: str) -> "Session":
        self.id = new_session_id
        for file in self.files:
            file.session_id = new_session_id
        for ring in self.rings:
            ring.reference.session_id = new_session_id
        return self

    def add_rehydration_tag(self) -> "Session":
        for file in self.files:
            if not "(re-hydrated)" in file.name_original:
                file.name_original = f"{file.name_original} (re-hydrated)"
        return self

    def delete_session_data(self) -> bool:
        session_directory = settings.WORK_DIRECTORY / self.id

        if session_directory.exists() and session_directory.is_dir():
            shutil.rmtree(session_directory)
            return True
        else:
            return False


##############
# CELERY TASKS
##############


class TaskStatus(StrEnum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PROCESSING = "PROCESSING"


class TaskResultType(StrEnum):
    SESSION = "SESSION"
    SESSION_FILE = "SESSION_FILE"
    BLAST_RING = "BLAST_RING"
    ANNOTATION_RING = "ANNOTATION_RING"
    LABEL_RING = "LABEL_RING"
    REFERENCE_RING = "REFERENCE_RING"
    GENOMAD_RING = "GENOMAD_RING"

    def from_model(
        model: (
            Session | SessionFile | BlastRing | AnnotationRing | LabelRing | GenomadRing
        ),
    ):
        if isinstance(model, Session):
            return TaskResultType.SESSION
        elif isinstance(model, SessionFile):
            return TaskResultType.SESSION_FILE
        elif isinstance(model, BlastRing):
            return TaskResultType.BLAST_RING
        elif isinstance(model, AnnotationRing):
            return TaskResultType.ANNOTATION_RING
        elif isinstance(model, LabelRing):
            return TaskResultType.LABEL_RING
        elif isinstance(model, ReferenceRing):
            return TaskResultType.REFERENCE_RING
        elif isinstance(model, GenomadRing):
            return TaskResultType.GENOMAD_RING
        else:
            raise TypeError("Could not determine task result return type from model")


class TaskStatusResponse(BaseModel):
    task_id: CeleryTaskID
    status: TaskStatus


class TaskResultResponse(TaskStatusResponse):
    result: Optional[
        Session
        | SessionFile
        | BlastRing
        | AnnotationRing
        | LabelRing
        | ReferenceRing
        | GenomadRing
    ]
    result_type: Optional[TaskResultType]


##############
# RING SCHEMAS
##############


class BlastMethod(StrEnum):
    BLASTN = "blastn"


class BlastRingSchema(RingSchema):
    genome_id: SessionFileID
    blast_method: BlastMethod = BlastMethod.BLASTN
    min_alignment: int = 0
    min_identity: float = 0.0
    min_evalue: float = 10.0

    @field_validator("genome_id")
    @classmethod
    def check_uuid_v4(cls, v: SessionFileID):
        try:
            UUID(v, version=4)
        except ValueError:
            raise ValueError(f"'{v}' is not a valid UUID4")

        return v

    @field_validator("reference")
    @classmethod
    def check_reference_file(cls, v: RingReference):
        if (
            v is not None
            and not (settings.WORK_DIRECTORY / v.session_id / v.reference_id).exists()
        ):
            raise ValueError(
                f"reference file could not be found. It may have been deleted or expired in session storage :("
            )
        return v

    @field_validator("min_alignment", mode="after")
    @classmethod
    def check_min_alignment(cls, v: int):
        if v < 0:
            raise ValueError("minimum alignment length must not be negative")

        return v

    @field_validator("min_identity", mode="after")
    @classmethod
    def check_min_identity(cls, v: float):
        if not 0.0 <= v <= 100.0:
            raise ValueError("minimum percent identity must be between 0 and 100")

        return v

    @field_validator("min_evalue", mode="after")
    @classmethod
    def check_min_evalue(cls, v: float):
        if v < 0:
            raise ValueError("minimum evalue must not be negative")
        return v

    # Do not use ValidationInfo - use model validator instead!

    @model_validator(mode="after")
    def check_genome_file(self) -> "BlastRingSchema":
        if not (
            settings.WORK_DIRECTORY / self.reference.session_id / self.genome_id
        ).exists():
            raise ValueError(
                f"genome comparison file could not be found. It may have been deleted or expired in session storage :("
            )
        return self

    def get_file_paths(self) -> Tuple[Path, Path, Path]:

        return (
            settings.WORK_DIRECTORY / self.reference.session_id,
            settings.WORK_DIRECTORY
            / self.reference.session_id
            / self.reference.reference_id,
            settings.WORK_DIRECTORY / self.reference.session_id / self.genome_id,
        )


class BlastRingResponse(BaseModel):
    task_id: CeleryTaskID


class AnnotationRingSchema(RingSchema):
    genbank_id: SessionFileID | None = None
    tsv_id: SessionFileID | None = None
    genbank_features: List[str] = []
    genbank_qualifiers: List[str] = []

    @field_validator("genbank_id", "tsv_id")
    @classmethod
    def check_uuid_v4(cls, v: SessionFileID):
        if v is not None:
            try:
                UUID(v, version=4)
            except ValueError:
                raise ValueError(f"'{v}' is not a valid UUIDv4")
        return v

    @model_validator(mode="after")
    def check_fields_and_files(self) -> "AnnotationRingSchema":

        if self.genbank_id is None and self.tsv_id is None:
            raise ValueError("one of 'genbank_id' or 'tsv_id' fields must be provided")

        if self.genbank_id:
            if not (
                settings.WORK_DIRECTORY / self.reference.session_id / self.genbank_id
            ).exists():
                raise ValueError(
                    f"genbank annotation file could not be found. It may have been deleted or expired in session storage :("
                )

        if self.tsv_id:
            if not (
                settings.WORK_DIRECTORY / self.reference.session_id / self.tsv_id
            ).exists():
                raise ValueError(
                    f"custom annotation file could not be found. It may have been deleted or expired in session storage :("
                )

        return self

    def get_file_paths(self) -> Tuple[Path, Path | None, Path | None]:

        return (
            settings.WORK_DIRECTORY / self.reference.session_id,
            (
                settings.WORK_DIRECTORY / self.reference.session_id / self.genbank_id
                if self.genbank_id
                else None
            ),
            (
                settings.WORK_DIRECTORY / self.reference.session_id / self.tsv_id
                if self.tsv_id
                else None
            ),
        )


class AnnotationRingResponse(BaseModel):
    task_id: CeleryTaskID


class LabelRingSchema(RingSchema):
    tsv_id: SessionFileID | None = None
    labels: List[RingSegment] = []

    @field_validator("tsv_id")
    @classmethod
    def check_uuid_v4(cls, v: SessionFileID):
        if v is not None:
            try:
                UUID(v, version=4)
            except ValueError:
                raise ValueError(f"'{v}' is not a valid UUIDv4")
        return v

    @model_validator(mode="after")
    def check_fields_and_files(self) -> "AnnotationRingSchema":

        if self.tsv_id is None and self.labels is None:
            raise ValueError("one of 'tsv_id' or 'labels' must be provided")

        if self.tsv_id:
            if not (
                settings.WORK_DIRECTORY / self.reference.session_id / self.tsv_id
            ).exists():
                raise ValueError(
                    f"custom annotation file could not be found. It may have been deleted or expired in session storage :("
                )

        return self

    def get_file_paths(self) -> Tuple[Path, Path | None]:

        return (
            settings.WORK_DIRECTORY / self.reference.session_id,
            (
                settings.WORK_DIRECTORY / self.reference.session_id / self.tsv_id
                if self.tsv_id
                else None
            ),
        )


class LabelRingResponse(BaseModel):
    task_id: CeleryTaskID


class ReferenceRingSchema(RingSchema):
    pass  # using the RingSchema.reference


class ReferenceRingResponse(BaseModel):
    task_id: CeleryTaskID


# Genomad ring


class GenomadRingSchema(RingSchema):

    window_size: int = 2500
    min_window_score: float = 0.0
    min_segment_score: float = 0.0
    min_segment_length: int = 0

    prediction_classes: List[GenomadPredictionClass] = [
        GenomadPredictionClass.PLASMID,
        GenomadPredictionClass.VIRUS,
    ]

    ring_type: RingType = RingType.LABEL

    @model_validator(mode="after")
    def check_reference_file(self):
        if not (
            settings.WORK_DIRECTORY
            / self.reference.session_id
            / self.reference.reference_id
        ).exists():
            raise ValueError(
                f"reference sequence file '{self.reference.reference_id}' does not exist"
            )

        if self.window_size < 2500:
            raise ValueError("Window size must be at least 3000 bp")
        if self.window_size > self.reference.sequence.length:
            raise ValueError(
                f"Window size cannot be larger than the reference sequence ({self.reference.sequence.length} bp)"
            )

        if self.ring_type not in (
            RingType.LABEL,
            RingType.ANNOTATION,
            RingType.GENOMAD,
        ):
            raise ValueError(
                f"Return ring type must be one of: {RingType.LABEL}, {RingType.ANNOTATION}, {RingType.GENOMAD}"
            )

        if not 0 <= self.min_segment_score <= 1:
            raise ValueError(f"Minimum segment score threshold must be between 0 and 1")

        if not 0 <= self.min_window_score <= 1:
            raise ValueError(f"Minimum segment score threshold must be between 0 and 1")

        if self.min_segment_length < 0:
            raise ValueError(f"Minimum segment length must be at least 0")

        return self

    def get_file_paths(self) -> Tuple[Path, Path]:

        return (
            settings.WORK_DIRECTORY / self.reference.session_id,
            settings.WORK_DIRECTORY
            / self.reference.session_id
            / self.reference.reference_id,
        )


class GenomadRingResponse(BaseModel):
    task_id: CeleryTaskID


# Ring Update


# Ring identifiers to update other indices for the
# current ring view (filtered by reference sequence
# in frontend) `index_other`
class RingUpdate(BaseModel):
    id: str
    index: int | None
    visible: bool | None
    color: str | None
    height: int | None
    title: str | None
    index_group: List[str] | None


# Label update schema for specific ring
class LabelUpdate(BaseModel):
    ring_id: str
    label_id: str
    lineLength: float | None = None
    lineWidth: float | None = None
    lineAngle: float | None = None
    lineColor: str | None = None
    text: str | None = None
    textSize: float | None = None
    textColor: str | None = None
