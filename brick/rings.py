from __future__ import annotations
from pydantic import BaseModel, Field
from pathlib import Path
from typing import List
from enum import StrEnum

from pydantic import BaseModel, validator

class RingType(StrEnum):
    GENERIC = 'generic'
    BLAST = 'blast'

class RingSegment(BaseModel):
    start: int
    end: int
    color: str = "#d3d3d3"
    text: str = ""

class Ring(BaseModel):
    index: int
    visible: bool = True
    color: str = "#d3d3d3"
    height: int = 20
    type: RingType = RingType.GENERIC
    title: str = "Ring"
    data: List[RingSegment] = Field(default_factory=list)

    def __init__(
        self, 
        index: int = -1, 
        visible: bool = True, 
        type: RingType = RingType.GENERIC, 
        color: str = "#d3d3d3", 
        height: int = 20, 
        title: str = "Ring",
        data: List[RingSegment] = []
    ):  
        """ Creates a default generic ring without segment data """
        super().__init__(
            index=index, 
            visible=visible, 
            type=type, 
            color=color, 
            height=height, 
            title=title,
            data=data
        )


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

    @validator('perc_identity')
    def check_perc_identity(cls, v):
        assert 0 <= v <= 100, 'Percentage identity must be between 0 and 100'
        return v

    @validator('e_value')
    def check_e_value(cls, v):
        assert v >= 0, 'E-value must be non-negative'
        return v
    
    def to_segment(self):
        return RingSegment(start=self.subject_start, end=self.subject_end)


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
    
    def from_blast_output(file: Path) -> BlastRing:
        return BlastRing(
            data=[entry.to_segment() for entry in parse_blastn_output(file)]
        )
    
