from __future__ import annotations

from pydantic import BaseModel, Field, validator
from statistics import mean
from strenum import StrEnum
from pathlib import Path
from typing import List, Generator, Tuple
from Bio import SeqIO

import pandas
import uuid
import csv

from .utils import sanitize_input


#######################
# ENUMS AND BASE MODELS
#######################


class RingType(StrEnum):
    GENERIC = "generic"
    BLAST = "blast"
    ANNOTATION = "annotation"
    LABEL = "label"
    REFERENCE = "reference"
    GENOMAD = "genomad"


class GenomadPredictionClass(StrEnum):
    CHROMOSOME = "chromosome"
    VIRUS = "virus"
    PLASMID = "plasmid"


class RingSegmentType(StrEnum):
    LABEL = "label"
    SEGMENT = "segment"
    GENOMAD = "genomad"


class RingSegment(BaseModel):
    start: int = 0
    end: int = 0
    text: str = ""


class GenomadSegment(RingSegment):
    plasmid: float | None = None
    virus: float | None = None
    chromosome: float | None = None


# Note camel-case need to change across
# front-end since this class was initially
# created due to changes in front-end
class LabelSegment(RingSegment):
    labelIdentifier: str
    lineLength: float | None = None
    lineWidth: float | None = None
    lineOpacity: float | None = None
    lineAngle: float | None = None
    lineColor: str | None = None
    textSize: float | None = None
    textColor: str | None = None
    textOpacity: str | None = None


class RingReferenceSequence(BaseModel):
    id: str = ""
    length: int = 0


class RingReference(BaseModel):
    session_id: str = ""
    reference_id: str = ""
    sequence: RingReferenceSequence = RingReferenceSequence()


class Ring(BaseModel):
    id: str
    index: int = -1
    visible: bool = True
    color: str = "#d3d3d3"
    height: int = 20
    type: RingType = RingType.GENERIC
    title: str = "Ring"
    reference: RingReference | None = None
    data: List[RingSegment | LabelSegment | GenomadSegment] = Field(
        default_factory=list
    )

    # Transformation like Session(**data) will select the first suitable
    # `data` field type, but we inherit LabelSegment and GenomadSegment
    # from RingSegment so that transformation will always return RingSegment.

    # Because the base RingSegment fields must be present even without inheritance
    # and the special segment fields can be `None`, it will return RingSegment
    # so we must use a validator to correct this based on presence of subclass
    # specific fields
    @validator("data", pre=True, each_item=True)
    @classmethod
    def set_correct_segment_type(cls, v):
        # Only apply if this is a dict from e.g. a database query to transform e.g. Session(**data)
        if type(v) == dict:
            if "textSize" in v:  # assuming this field is unique to LabelSegment
                return LabelSegment(**v)
            elif "plasmid" in v:  # assuming this field is unique to GenomadSegment
                return GenomadSegment(**v)
            else:  # default if no unique fields are found is RingSegment
                return RingSegment(**v)
        return v


class BlastnEntry(BaseModel):
    query_id: str
    subject_id: str
    perc_identity: float
    alignment_length: int
    mismatches: int
    gap_opens: int
    query_start: int
    query_end: int
    subject_start: int
    subject_end: int
    e_value: float
    bit_score: float

    def to_segment(self):
        return RingSegment(
            start=self.subject_start,
            end=self.subject_end,
            text=f"{self.perc_identity:.2f}% nucleotide identity",
        )


class GenBankFeatureEntry(BaseModel):
    start: int
    end: int
    annotation: str

    def to_segment(
        self,
        sanitize: bool = True,
        segment_type: RingSegmentType = RingSegmentType.SEGMENT,
    ) -> RingSegment | LabelSegment:
        if segment_type == RingSegmentType.SEGMENT:
            return RingSegment(
                start=self.start,
                end=self.end,
                text=(
                    sanitize_input(
                        input_string=self.annotation, is_for_db=True, is_for_svg=True
                    )
                    if sanitize
                    else self.annotation
                ),
            )
        elif segment_type == RingSegmentType.GENOMAD:
            return LabelRing(
                start=self.start,
                end=self.end,
                text=(
                    sanitize_input(
                        input_string=self.annotation, is_for_db=True, is_for_svg=True
                    )
                    if sanitize
                    else self.annotation
                ),
            )
        else:
            raise ValueError(f"Ring segment type {RingSegmentType.LABEL} not supported")


class GenomadEntry(BaseModel):
    seq_name: str
    start: int
    end: int
    chromosome_score: float
    plasmid_score: float
    virus_score: float

    def to_segment(
        self,
        prediction_classes: List[GenomadPredictionClass],
        min_window_score: float = 0.7,
    ):

        label = ""
        if (
            self.chromosome_score >= min_window_score
            and GenomadPredictionClass.CHROMOSOME in prediction_classes
        ):
            label += f"Chromosome ({self.chromosome_score:.2f}) "
        else:
            self.chromosome_score = 0

        if (
            self.plasmid_score >= min_window_score
            and GenomadPredictionClass.PLASMID in prediction_classes
        ):
            label += f"Plasmid ({self.plasmid_score:.2f}) "
        else:
            self.plasmid_score = 0

        if (
            self.virus_score >= min_window_score
            and GenomadPredictionClass.VIRUS in prediction_classes
        ):
            label += f"Virus ({self.virus_score:.2f}) "
        else:
            self.virus_score = 0

        return GenomadSegment(
            start=self.start,
            end=self.end,
            text=label,
            plasmid=self.plasmid_score,
            chromosome=self.chromosome_score,
            virus=self.virus_score,
        )


##################
# HELPER FUNCTIONS
##################


def parse_blastn_output(
    file_path: Path,
    reference: RingReference | None = None,
    min_identity: int = 0,
    min_alignment: int = 0,
    min_evalue: float = 0,
) -> List[BlastnEntry]:
    """
    Parses a BLASTn output file with `-outfmt 6` format.

    Args:
    file_path (FilePath): The path to the BLASTn output file.

    Returns:
    List[BlastnEntry]: A list of BlastnEntry models representing each line in the BLASTn output.
    """
    result = []

    with file_path.open("r") as file:
        for line in file:
            fields = line.strip().split("\t")
            entry = BlastnEntry(
                query_id=fields[0],
                subject_id=fields[1],
                perc_identity=float(fields[2]),
                alignment_length=int(fields[3]),
                mismatches=int(fields[4]),
                gap_opens=int(fields[5]),
                query_start=int(fields[6]),
                query_end=int(fields[7]),
                subject_start=int(fields[8]),
                subject_end=int(fields[9]),
                e_value=float(fields[10]),
                bit_score=float(fields[11]),
            )
            if entry.perc_identity < min_identity:
                continue
            if entry.alignment_length < min_alignment:
                continue
            if entry.e_value > min_evalue:
                continue

            if reference:
                if entry.subject_id == reference.sequence.id:
                    result.append(entry)
            else:
                result.append(entry)

    return result


# Generator function
def parse_aggregated_genomad_output(file: Path) -> Generator[GenomadEntry]:
    """
    Parses the aggregated_classification output from a sliced genome file
    """

    genomad_output = pandas.read_csv(file, sep="\t", header=0)
    for _, row in genomad_output.iterrows():

        start, end, seq_id = get_start_end_from_seq_name(seq_name=row["seq_name"])

        yield GenomadEntry(
            seq_name=seq_id,
            start=start,
            end=end,
            chromosome_score=row["chromosome_score"],
            plasmid_score=row["plasmid_score"],
            virus_score=row["virus_score"],
        )


def extract_genomad_contiguous_segments(
    file: Path,
    min_segment_score: float,  # minimum mean score of a contiguous segment to consider returning a segment
    min_window_score: float,  # minimum score to consider slice as part of contiguous segment for prediction class
    min_segment_length: int,  # should be a multiple of slice length
    prediction_classes: List[GenomadPredictionClass],
    segment_type: RingSegmentType,
) -> Generator[RingSegment] | Generator[LabelSegment]:
    """Extracts segments of high probabilty for each prediction class with a minimum total length for label or annotation rings"""

    segments = []

    genomad_output = pandas.read_csv(file, sep="\t", header=0)

    def process_column(column: str):
        prediction_class = column.replace("_score", "")

        current_probabilities = []
        current_segment = None
        for _, row in genomad_output.iterrows():

            try:
                probability = float(row[column])
            except ValueError:
                raise ValueError("Probability could not be converted to float type")

            start, end, _ = get_start_end_from_seq_name(seq_name=row["seq_name"])

            # Contiguous segment checks and dictionary insertions
            if probability >= min_window_score:
                if current_segment is None:
                    if segment_type == RingSegmentType.SEGMENT:
                        current_segment = RingSegment(start=start, end=end)
                    elif segment_type == RingSegmentType.LABEL:
                        current_segment = LabelSegment(
                            start=start, end=end, labelIdentifier=str(uuid.uuid4())
                        )
                    else:
                        raise ValueError(
                            f"Segment type {segment_type} not supported for extracting contiguous segment annotations from Genomad"
                        )

                    current_probabilities = [probability]
                else:
                    current_segment.end = end
                    current_probabilities.append(probability)
            else:
                if current_segment and (
                    current_segment.end - current_segment.start >= min_segment_length
                ):

                    prediction_class_label = (
                        "Phage"
                        if prediction_class == GenomadPredictionClass.VIRUS
                        else prediction_class.capitalize()
                    )
                    current_segment.text = (
                        f"{prediction_class_label} ({mean(current_probabilities):.2f})"
                    )

                    mean_segment_score = mean(current_probabilities)
                    if (
                        prediction_class in prediction_classes
                        and mean_segment_score >= min_segment_score
                    ):
                        segments.append(current_segment)

                current_segment = None

        # Check for a segment at the end
        if current_segment and (
            current_segment.end - current_segment.start >= min_segment_length
        ):
            if prediction_class in prediction_classes:
                segments.append(current_segment)

    process_column("chromosome_score")
    process_column("plasmid_score")
    process_column("virus_score")

    for segment in sorted(segments, key=lambda segment: segment.start):
        yield segment


def get_start_end_from_seq_name(
    seq_name: str, name_split: str = "__", range_split: str = ".."
) -> Tuple[int, int, str]:

    try:
        seq_id: str = seq_name.split(name_split)[0]
        seq_range: str = seq_name.split(name_split)[1]
    except IndexError:
        raise IndexError(
            "Could not split the sequence name to extract sequence range - was the file sliced?"
        )

    start_end: str = seq_range.split(range_split)
    if len(start_end) != 2:
        raise ValueError(
            "Could not extract start and end positions from sequence range in sequence name - was the file sliced?"
        )

    try:
        start, end = [int(v) for v in start_end]
    except ValueError:
        raise ValueError(
            "Start or end value could not be converted to integer type - is the range format correct?"
        )

    return start, end, seq_id


def parse_genbank_features(
    file_path: str, feature_types: List[str]
) -> List[GenBankFeatureEntry]:
    entries = []

    # Parse the GenBank file
    for record in SeqIO.parse(file_path, "genbank"):
        # Iterate over the features
        for feature in record.features:
            if feature.type in feature_types:
                # Extract the desired information
                start = int(feature.location.start)
                end = int(feature.location.end)
                annotation = feature.type

                # Add extra annotations if available
                if "gene" in feature.qualifiers:
                    annotation += f" {feature.qualifiers['gene'][0]}"

                if "product" in feature.qualifiers:
                    annotation += f" {feature.qualifiers['product'][0]}"

                entries.append(
                    GenBankFeatureEntry(start=start, end=end, annotation=annotation)
                )

    return entries


def parse_tsv_segments(
    file_path: Path,
    sanitize: bool = True,
    segment_type: RingSegmentType = RingSegmentType.SEGMENT,
) -> List[LabelSegment] | List[RingSegment]:

    segments = []
    with file_path.open(mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="\t")

        for row in reader:
            if segment_type == RingSegmentType.SEGMENT:
                segment = RingSegment(
                    start=int(row["start"]),
                    end=int(row["end"]),
                    text=(
                        sanitize_input(
                            input_string=row["text"], is_for_db=True, is_for_svg=True
                        )
                        if sanitize
                        else row["text"]
                    ),
                )
            elif segment_type == RingSegmentType.LABEL:
                segment = LabelSegment(
                    start=int(row["start"]),
                    end=int(row["end"]),
                    text=(
                        sanitize_input(
                            input_string=row["text"], is_for_db=True, is_for_svg=True
                        )
                        if sanitize
                        else row["text"]
                    ),
                    labelIdentifier=str(uuid.uuid4()),
                )
            else:
                raise ValueError(f"Segment type {segment_type} not supported")

            segments.append(segment)
    return segments


#############
# RING MODELS
#############


class ReferenceRing(Ring):
    type: RingType = RingType.REFERENCE
    title: str = "Reference Ring"

    @staticmethod
    def from_reference(reference: RingReference) -> ReferenceRing:
        return ReferenceRing(
            id=str(uuid.uuid4()),
            data=[
                RingSegment(
                    start=0, end=reference.sequence.length, text=reference.sequence.id
                )
            ],
            reference=reference,
        )


class BlastRing(Ring):
    type: RingType = RingType.BLAST
    title: str = "BLAST Ring"

    @staticmethod
    def from_blast_output(
        file: Path,
        reference: RingReference | None = None,
        min_identity: int = 0,
        min_alignment: int = 0,
        min_evalue: float = 0,
    ) -> BlastRing:
        return BlastRing(
            id=str(uuid.uuid4()),
            data=[
                entry.to_segment()
                for entry in parse_blastn_output(
                    file_path=file,
                    reference=reference,
                    min_identity=min_identity,
                    min_alignment=min_alignment,
                    min_evalue=min_evalue,
                )
            ],
            reference=reference,
        )


class LabelRing(Ring):
    data: List[LabelSegment] = Field(default_factory=list)
    type: RingType = RingType.LABEL
    title: str = "Label Ring"

    @staticmethod
    def from_genbank_file(
        file: Path,
        features: List[str],
        reference: RingReference | None = None,
        sanitize: bool = True,
    ) -> LabelRing:
        return LabelRing(
            id=str(uuid.uuid4()),
            data=[
                entry.to_segment(sanitize=sanitize, segment_type=RingSegmentType.LABEL)
                for entry in parse_genbank_features(
                    file_path=str(file), feature_types=features
                )
            ],
            reference=reference,
        )

    @staticmethod
    def from_tsv_file(
        file: Path, reference: RingReference | None = None, sanitize: bool = True
    ) -> LabelRing:
        return LabelRing(
            id=str(uuid.uuid4()),
            data=[
                segment
                for segment in parse_tsv_segments(
                    file_path=file,
                    sanitize=sanitize,
                    segment_type=RingSegmentType.LABEL,
                )
            ],
            reference=reference,
        )

    def add_custom_labels(
        self, labels: List[LabelSegment], sanitize: bool = True
    ) -> None:

        for segment in labels:
            if sanitize:
                segment.text = sanitize_input(
                    input_string=segment.text, is_for_db=True, is_for_svg=True
                )
            self.data.append(segment)

    @staticmethod
    def from_genomad_output(
        file: Path,
        reference: RingReference | None = None,
        min_window_score: float = 0.5,
        min_segment_score: float = 0.7,
        min_segment_length: int = 10000,  # should be a multiple of GenomadRingSchema.window_size
        prediction_classes: List[GenomadPredictionClass] = [
            GenomadPredictionClass.VIRUS,
            GenomadPredictionClass.PLASMID,
        ],
    ) -> LabelRing:
        return LabelRing(
            id=str(uuid.uuid4()),
            data=[
                segment
                for segment in extract_genomad_contiguous_segments(
                    file=file,
                    min_segment_length=min_segment_length,
                    min_window_score=min_window_score,
                    min_segment_score=min_segment_score,
                    prediction_classes=prediction_classes,
                    segment_type=RingSegmentType.LABEL,
                )
            ],
            reference=reference,
        )


class AnnotationRing(Ring):
    type: RingType = RingType.ANNOTATION
    title: str = "Annotation Ring"

    def from_genbank_file(
        file: Path,
        features: List[str],
        reference: RingReference | None = None,
        sanitize: bool = True,
    ) -> AnnotationRing:
        return AnnotationRing(
            id=str(uuid.uuid4()),
            data=[
                entry.to_segment(
                    sanitize=sanitize, segment_type=RingSegmentType.SEGMENT
                )
                for entry in parse_genbank_features(
                    file_path=str(file), feature_types=features
                )
            ],
            reference=reference,
        )

    def from_tsv_file(
        file: Path, reference: RingReference | None = None, sanitize: bool = True
    ) -> AnnotationRing:
        return AnnotationRing(
            id=str(uuid.uuid4()),
            data=[
                segment
                for segment in parse_tsv_segments(
                    file_path=file,
                    sanitize=sanitize,
                    segment_type=RingSegmentType.SEGMENT,
                )
            ],
            reference=reference,
        )

    @staticmethod
    def from_genomad_output(
        file: Path,
        reference: RingReference | None = None,
        min_window_score: float = 0.5,
        min_segment_score: float = 0.7,
        min_segment_length: int = 10000,  # should be a multiple of GenomadRingSchema.window_size
        prediction_classes: List[GenomadPredictionClass] = [
            GenomadPredictionClass.VIRUS,
            GenomadPredictionClass.PLASMID,
        ],
    ) -> AnnotationRing:
        return AnnotationRing(
            id=str(uuid.uuid4()),
            data=[
                segment
                for segment in extract_genomad_contiguous_segments(
                    file=file,
                    min_segment_length=min_segment_length,
                    min_window_score=min_window_score,
                    min_segment_score=min_segment_score,
                    prediction_classes=prediction_classes,
                    segment_type=RingSegmentType.SEGMENT,
                )
            ],
            reference=reference,
        )


class GenomadRing(Ring):
    data: List[GenomadSegment] = Field(default_factory=list)
    type: RingType = RingType.GENOMAD
    title: str = "Genomad Ring"

    @staticmethod
    def from_genomad_output(
        file: Path,
        reference: RingReference | None = None,
        min_window_score: float = 0,
        prediction_classes: List[GenomadPredictionClass] = [
            GenomadPredictionClass.VIRUS,
            GenomadPredictionClass.PLASMID,
        ],
    ) -> GenomadRing:
        return GenomadRing(
            id=str(uuid.uuid4()),
            data=[
                entry.to_segment(
                    prediction_classes=prediction_classes,
                    min_window_score=min_window_score,
                )
                for entry in parse_aggregated_genomad_output(file=file)
            ],
            reference=reference,
        )
