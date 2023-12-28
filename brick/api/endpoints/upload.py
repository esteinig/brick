import shutil
import os
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from celery.result import AsyncResult

from ..schemas import FileConfig
from ..core.config import settings
from ..core.celery import celery_app
from ..tasks import process_file

router = APIRouter(
    prefix="/files",
    tags=["files"],
)

def safe_filename(filename: str) -> str:
    """Generate a safe filename to prevent directory traversal attacks."""
    return str(uuid.uuid4()) + os.path.splitext(filename)[-1]

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), config: str = Form(...)):

    try:
        config_data = FileConfig.parse_raw(config)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid config data: {e}")

    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file uploaded")

    session_directory: Path = settings.WORK_DIRECTORY / config_data.session_id    
    file_path = session_directory / safe_filename(file.filename)

    if not session_directory.exists():
        session_directory.mkdir(parents=True)

    # TODO: Implement directory size limits per session

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    try:
        task = process_file.delay(str(file_path), config_data.dict(), file.filename)
    except Exception as e:
        # Delete the file since the task failed to initiate
        file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error initiating task: {str(e)}")

    return JSONResponse(status_code=202, content={"task_id": task.id, "status": "SUCCESS"})

@router.get("/status/{task_id}")
def get_task_status(task_id: str):

    task_result = AsyncResult(task_id, app=celery_app)

    return {"task_id": task_id, "status": task_result.status}

@router.get("/result/{task_id}")
def get_task_result(task_id: str):

    task_result = AsyncResult(task_id, app=celery_app)

    if not task_result.ready():
        return JSONResponse(status_code=202, content={"task_id": task_id, "status": "PROCESSING"})

    result = task_result.get()

    if result["success"]:
        return JSONResponse(status_code=202, content={"task_id": task_id, "task_result": result["result"], "status": "SUCCESS"})
    else:
        raise HTTPException(status_code=500, detail=result["error"])
