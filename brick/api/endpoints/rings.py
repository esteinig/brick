from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException

from ..schemas import BlastRingSchema, BlastRingResponse
from ..schemas import AnnotationRingSchema, AnnotationRingResponse
from ..schemas import LabelRingSchema, LabelRingResponse
from ..schemas import ReferenceRingSchema, ReferenceRingResponse
from ..schemas import GenomadRingSchema, GenomadRingResponse
from ..tasks import (
    process_blast_ring,
    process_annotation_ring,
    process_label_ring,
    process_reference_ring,
    process_genomad_ring,
)


router = APIRouter(
    prefix="/rings",
    tags=["ring"],
)


@router.post("/reference", response_model=ReferenceRingResponse)
def create_reference_ring(ring_config: ReferenceRingSchema):

    try:
        task = process_reference_ring.delay(ring_config.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initiating task: {str(e)}")

    return JSONResponse(
        status_code=202, content=BlastRingResponse(task_id=task.id).model_dump()
    )


@router.post("/blast", response_model=BlastRingResponse)
def create_blast_ring(ring_config: BlastRingSchema):

    _, reference_file, genome_file = ring_config.get_file_paths()

    try:
        task = process_blast_ring.delay(
            str(reference_file), str(genome_file), ring_config.model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initiating task: {str(e)}")

    return JSONResponse(
        status_code=202, content=BlastRingResponse(task_id=task.id).model_dump()
    )


@router.post("/annotation", response_model=AnnotationRingResponse)
def create_annotation_ring(ring_config: AnnotationRingSchema):

    _, genbank_file, tsv_file = ring_config.get_file_paths()

    try:
        task = process_annotation_ring.delay(
            str(genbank_file) if genbank_file else None,
            str(tsv_file) if tsv_file else None,
            ring_config.model_dump(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initiating task: {str(e)}")

    return JSONResponse(
        status_code=202, content=AnnotationRingResponse(task_id=task.id).model_dump()
    )


@router.post("/label", response_model=LabelRingResponse)
def create_label_ring(ring_config: LabelRingSchema):

    _, tsv_file = ring_config.get_file_paths()

    try:
        task = process_label_ring.delay(
            str(tsv_file) if tsv_file else None, ring_config.model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initiating task: {str(e)}")

    return JSONResponse(
        status_code=202, content=LabelRingResponse(task_id=task.id).model_dump()
    )


@router.post("/genomad", response_model=GenomadRingResponse)
def create_label_ring(ring_config: GenomadRingSchema):

    _, reference_file = ring_config.get_file_paths()

    try:
        task = process_genomad_ring.delay(str(reference_file), ring_config.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initiating task: {str(e)}")

    return JSONResponse(
        status_code=202, content=GenomadRingResponse(task_id=task.id).model_dump()
    )
