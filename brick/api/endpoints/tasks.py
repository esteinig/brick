from celery.result import AsyncResult
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException

from ..schemas import TaskStatus, TaskStatusResponse, TaskResultResponse
from ..core.celery import celery_app

router = APIRouter(
    prefix="/tasks",
    tags=["task", "celery"],
)


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
def get_task_status(task_id: str):
    """ 
    Query file upload processing status
    """
    task_result = AsyncResult(task_id, app=celery_app)

    return {"task_id": task_id, "status": task_result.status}


@router.get("/result/{task_id}")
def get_task_result(task_id: str):
    """ 
    Query file upload processing result
    """
    task_result = AsyncResult(task_id, app=celery_app)

    if not task_result.ready():
        return JSONResponse(
            status_code=202, 
            content=TaskResultResponse(
                task_id=task_id, 
                status=TaskStatus.PROCESSING, 
                result=None
            ).model_dump()
        )
    
    result = task_result.get()

    if result["success"]:
        return JSONResponse(
            status_code=200, 
            content=TaskResultResponse(
                task_id=task_id, 
                status=TaskStatus.SUCCESS, 
                result=result["result"]
            ).model_dump()
        )
    else:
        raise HTTPException(status_code=500, detail=result["error"])