from typing import List
from pydantic import BaseModel
from .schemas import SessionFile

class Figure(BaseModel):
    id: str

class Session(BaseModel):
    id: str
    created: str
    files: List[SessionFile]
    figure: Figure