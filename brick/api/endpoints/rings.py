from fastapi.responses import JSONResponse
from fastapi import APIRouter,  HTTPException

from ..schemas import BlastRingSchema, BlastRingResponse
from ..schemas import AnnotationRingSchema, AnnotationRingResponse
from ..tasks import process_blast_ring, process_annotation_ring


router = APIRouter(
    prefix="/rings",
    tags=["ring"],
)


@router.post("/blast")
def create_blast_ring(ring_config: BlastRingSchema):
    
    _, reference_file, genome_file = ring_config.get_file_paths()

    try:
        task = process_blast_ring.delay(
            str(reference_file), 
            str(genome_file), 
            ring_config.model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initiating task: {str(e)}")

    return JSONResponse(
        status_code=202, 
        content=BlastRingResponse(
            task_id=task.id
        ).model_dump()
    )

@router.post("/annotation")
def create_annotation_ring(ring_config: AnnotationRingSchema):
    
    _, genbank_file, tsv_file = ring_config.get_file_paths()

    try:
        task = process_annotation_ring.delay(
            str(genbank_file), 
            str(tsv_file), 
            ring_config.model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initiating task: {str(e)}")

    return JSONResponse(
        status_code=202, 
        content=AnnotationRingResponse(
            task_id=task.id
        ).model_dump()
    )