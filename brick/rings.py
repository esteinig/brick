from __future__ import annotations
from pydantic import BaseModel, Field
from pathlib import Path
from typing import List
from enum import StrEnum
from Bio import SeqIO

import csv
from pydantic import BaseModel

from .utils import sanitize_input

class RingType(StrEnum):
    GENERIC = 'generic'
    BLAST = 'blast'
    ANNOTATION = 'annotation'
    LABEL = 'label'

class RingSegment(BaseModel):
    start: int
    end: int
    color: str = "#d3d3d3"
    text: str = ""

class Ring(BaseModel):
    index: int = -1
    visible: bool = True
    color: str = "#d3d3d3"
    height: int = 20
    type: RingType = RingType.GENERIC
    title: str = "Ring"
    data: List[RingSegment] = Field(default_factory=list)


# Blast Ring
        
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
            start=self.subject_start, end=self.subject_end,
            text=f"Identity: {self.perc_identity:.2}%  E-value: {self.e_value}"
        )


def parse_blastn_output(file_path: Path) -> List[BlastnEntry]:
    """
    Parses a BLASTn output file with `-outfmt 6` format.
    
    Args:
    file_path (FilePath): The path to the BLASTn output file.

    Returns:
    List[BlastnEntry]: A list of BlastnEntry models representing each line in the BLASTn output.
    """
    result = []

    with file_path.open('r') as file:
        for line in file:
            fields = line.strip().split('\t')
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
                bit_score=float(fields[11])
            )
            result.append(entry)

    return result


class BlastRing(Ring):
    type: RingType = RingType.BLAST
    title: str = "BLAST Ring"
    
    @staticmethod
    def from_blast_output(file: Path) -> BlastRing:
        return BlastRing(
            data=[entry.to_segment() for entry in parse_blastn_output(file_path=file)]
        )
    
# Annotation Rings
    
class GenBankFeatureEntry(BaseModel):
    start: int
    end: int
    annotation: str

    def to_segment(self, sanitize: bool = True) -> RingSegment:
        return RingSegment(
            start=self.start,
            end=self.end,
            text=sanitize_input(
                input_string=self.annotation, 
                is_for_db=True, 
                is_for_svg=True
            ) if sanitize else self.annotation
        )

def parse_genbank_features(file_path: str, feature_types: List[str]) -> List[GenBankFeatureEntry]:
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
                if 'gene' in feature.qualifiers:
                    annotation += f" Gene: {feature.qualifiers['gene'][0]})"

                if 'product' in feature.qualifiers:
                    annotation += f"  Product: {feature.qualifiers['product'][0]}"

                entries.append(GenBankFeatureEntry(start=start, end=end, annotation=annotation))

    return entries

def parse_tsv_segments(file_path: Path, sanitize: bool = True) -> List[RingSegment]:
    segments = []

    with file_path.open(mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')

        for row in reader:
            segment = RingSegment(
                start=int(row['start']),
                end=int(row['end']),
                text=sanitize_input(
                    input_string=row['text'],
                    is_for_db=True, 
                    is_for_svg=True
                ) if sanitize else row['text'],
                color=sanitize_input(
                    input_string=row['color'],
                    is_for_db=True, 
                    is_for_svg=True
                ) if sanitize else row['color'],
            )
            segments.append(segment)

    return segments

class AnnotationRing(Ring):
    type: RingType = RingType.ANNOTATION
    title: str = "Annotation Ring"
    
    def from_genbank_file(file: Path, features: List[str], sanitize: bool = True) -> AnnotationRing:
        return AnnotationRing(
            data=[entry.to_segment(sanitize=sanitize) for entry in parse_genbank_features(
                file_path=str(file), feature_types=features
            )]
        )
    
    def from_tsv_file(file: Path, sanitize: bool = True) -> AnnotationRing:
        return AnnotationRing(
            data=[segment for segment in parse_tsv_segments(file_path=file, sanitize=sanitize)]
        )
    
class LabelRing(Ring):
    type: RingType = RingType.LABEL
    title: str = "Label Ring"
    
    def from_genbank_file(file: Path, features: List[str], sanitize: bool = True) -> LabelRing:
        return LabelRing(
            data=[entry.to_segment(sanitize=sanitize) for entry in parse_genbank_features(
                file_path=str(file), feature_types=features
            )]
        )
    
    def from_tsv_file(file: Path, sanitize: bool = True) -> LabelRing:
        return LabelRing(
            data=[segment for segment in parse_tsv_segments(file_path=file, sanitize=sanitize)]
        )
    
    def add_manual_labels(self, labels: List[RingSegment], sanitize: bool = True) -> None:

        for segment in labels:
            if sanitize:
                segment.text = sanitize_input(
                    input_string=segment.text,
                    is_for_db=True, is_for_svg=True
                )
                segment.color = sanitize_input(
                    input_string=segment.color,
                    is_for_db=True, is_for_svg=True
                )
            self.data.append(segment)