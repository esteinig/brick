from typing import List
from pydantic import BaseModel
from .schemas import SessionFile

class Session(BaseModel):
    id: str
    date: str
    files: List[SessionFile]