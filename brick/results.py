from pydantic import BaseModel, validator

from .rings import RingSegment

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
    
    def to_ring_segment(self):
        return RingSegment(start=self.subject_start, end=self.subject_end)