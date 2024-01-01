import shutil
import os
import uuid

from pathlib import Path
from typing import List

from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from ..schemas import FileConfig, UploadFileResponse
from ..models import Session, SessionFile

from ..core.config import settings

from ..core.db import get_session_collection_motor
from ..utils import sanitize_input
from ..tasks import process_file

router = APIRouter(
    prefix="/files",
    tags=["file", "upload"],
)


@router.get("/{session_id}", response_model=List[SessionFile])
async def get_files(session_id: str):

    collection = await get_session_collection_motor()
    session_data = await collection.find_one({"id": session_id})

    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")

    del session_data["_id"]

    return Session(**session_data).files


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), config: str = Form(...)):
    """
    Upload a file for initial validation and processing
    """

    # File configuration provided as form data
    try:
        config_data = FileConfig.model_validate_json(config)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid config data: {e}")

    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Session directory checks
    session_directory: Path = settings.WORK_DIRECTORY / config_data.session_id    

    if not session_directory.exists():
        session_directory.mkdir(parents=True)
        
    try:
        if not is_safe_to_add_files(
            directory_path=session_directory, 
            max_files_allowed=settings.SESSION_MAX_FILES, 
            max_dir_size_mb=settings.SESSION_MAX_SIZE_MB
        ):
            raise HTTPException(status_code=500, detail=f"Error uploading file: session has reached capacity")
    except NotADirectoryError as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

    # Sanitize filename

    sanitized_filename = sanitize_input(
        input_string=file.filename,
        is_for_db=True,
        is_for_svg=False
    )

    # Save file and initate processing
    file_path = session_directory / safe_filename()

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    try:
        task = process_file.delay(str(file_path), config_data.model_dump(), sanitized_filename)
    except Exception as e:
        file_path.unlink() # delete the file since the task failed to initiate
        raise HTTPException(status_code=500, detail=f"Error initiating task: {str(e)}")

    return JSONResponse(
        status_code=202, 
        content=UploadFileResponse(
            task_id=task.id
        ).model_dump()
    )

# Helpers

def safe_filename() -> str:
    """
    Generate a safe filename to prevent directory traversal attacks
    """
    return str(uuid.uuid4())


def is_safe_to_add_files(directory_path: Path, max_files_allowed: int, max_dir_size_mb: int) -> bool:
    """
    Check if the number of files and the total size of a directory do not exceed specified limits
    """
    directory = Path(directory_path)

    if not directory.is_dir():
        raise NotADirectoryError(f"{directory_path} is not a directory.")

    file_count = sum(1 for file in directory.glob('**/*') if file.is_file())
    total_size = sum(file.stat().st_size for file in directory.glob('**/*') if file.is_file())
    total_size_mb = total_size / (1024 * 1024)

    return file_count < max_files_allowed and total_size_mb < max_dir_size_mb
