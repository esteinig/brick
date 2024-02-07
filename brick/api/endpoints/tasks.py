from celery.result import AsyncResult
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException

from ..schemas import TaskStatus, TaskStatusResponse, TaskResultResponse
from ..core.celery import celery_app
from ..schemas import Session, SessionFile, FileFormat, TaskResultType
from ...rings import (
    ReferenceRing,
    BlastRing,
    AnnotationRing,
    LabelRing,
    GenomadRing,
    RingType,
)

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
                result=None,
                result_type=None,
            ).model_dump(),
        )

    result = task_result.get()

    if result["success"]:

        # Task result outputs are always dictionaries
        if isinstance(result["result"], dict):
            result_data = result["result"]
        else:
            raise TypeError("Output of the requested task was not a dictionary")

        try:
            result_model = get_result_model(result_data=result_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return JSONResponse(
            status_code=200,
            content=TaskResultResponse(
                task_id=task_id,
                status=TaskStatus.SUCCESS,
                result=result_model,
                result_type=TaskResultType.from_model(
                    model=result_model
                ),  # add types here if adding new tasks
            ).model_dump(),
        )
    else:
        raise HTTPException(status_code=500, detail=result["error"])


def get_result_model(
    result_data: dict,
) -> (
    Session
    | SessionFile
    | BlastRing
    | AnnotationRing
    | ReferenceRing
    | GenomadRing
    | LabelRing
):
    """
    Identification of result models from a common result endpoint for tasks exceuted with Celery
    """

    if "format" in result_data and any(
        result_data["format"] == item.value for item in FileFormat
    ):
        return SessionFile(**result_data)
    elif "type" in result_data and result_data["type"] == RingType.BLAST:
        return BlastRing(**result_data)
    elif "type" in result_data and result_data["type"] == RingType.ANNOTATION:
        return AnnotationRing(**result_data)
    elif "type" in result_data and result_data["type"] == RingType.LABEL:
        return LabelRing(**result_data)
    elif "type" in result_data and result_data["type"] == RingType.REFERENCE:
        return ReferenceRing(**result_data)
    elif "type" in result_data and result_data["type"] == RingType.GENOMAD:
        return GenomadRing(**result_data)
    elif "date" in result_data:
        return Session(**result_data)
    else:
        raise TypeError("Task result did not match a known model")
