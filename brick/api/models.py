from typing import List
from pydantic import BaseModel
from .schemas import SessionFile
from .core.config import settings

class Session(BaseModel):
    id: str
    date: str
    files: List[SessionFile]

    def validate_file_paths(self):
        for file in self.files:
            file_path = settings.WORK_DIRECTORY / file.session_id / file.id
            if not file_path.exists():
                raise FileNotFoundError(f"Could not find file `{file.name_original}` in session directory path: {file_path}")
