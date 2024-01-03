from celery.result import AsyncResult
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException

from ..schemas import TaskStatus, TaskStatusResponse, TaskResultResponse
from ..core.celery import celery_app
from ..schemas import SessionFile
from ...rings import BlastRing, AnnotationRing, LabelRing, RingType

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
        if isinstance(result["result"], dict):
            result_data = result["result"]

            if 'session_id' in result_data:
                result_model = SessionFile(**result_data)
            elif 'type' in result_data and result_data["type"] == RingType.BLAST:
                result_model = BlastRing(**result_data)
            elif 'type' in result_data and result_data["type"] == RingType.ANNOTATION:
                result_model = AnnotationRing(**result_data)
            elif 'type' in result_data and result_data["type"] == RingType.LABEL:
                result_model = LabelRing(**result_data)
            else: 
                raise HTTPException(status_code=500, detail="Task result did not have a known type")

        return JSONResponse(
            status_code=200, 
            content=TaskResultResponse(
                task_id=task_id, 
                status=TaskStatus.SUCCESS, 
                result=result_model
            ).model_dump()
        )
    else:
        raise HTTPException(status_code=500, detail=result["error"])