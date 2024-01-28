import pytest
import shutil
import uuid

from pathlib import Path
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from brick.api.main import app, settings

from brick.rings import RingReference
from brick.api.schemas import BlastRingSchema, BlastRingResponse
from brick.api.schemas import AnnotationRingSchema, AnnotationRingResponse
from brick.api.schemas import LabelRingSchema, LabelRingResponse


def create_mock_session_directory(session_id: str) -> Path:
    tmp = Path(settings.WORK_DIRECTORY / session_id)
    tmp.mkdir(parents=True)
    return tmp


def create_mock_session_file(session_id: str) -> Path:
    file_path = settings.WORK_DIRECTORY / session_id / str(uuid.uuid4())
    file_path.touch()
    return file_path


@pytest.fixture()
def mock_label_ring_data():

    mock_label_ring_tmpdir = create_mock_session_directory(str(uuid.uuid4()))
    session_id = mock_label_ring_tmpdir.name

    mock_label_ring_schema = LabelRingSchema(
        reference=RingReference(session_id=session_id),
        tsv_id=create_mock_session_file(session_id=session_id).name,
    )

    mock_label_ring_response = LabelRingResponse(task_id="some_task_id")

    yield mock_label_ring_schema, mock_label_ring_response

    # Cleanup after tests deleting temporary session directory tree
    shutil.rmtree(mock_label_ring_tmpdir)


@pytest.mark.asyncio
@patch("brick.api.endpoints.rings.process_label_ring")
async def test_create_label_ring_success(mock_process_label_ring, mock_label_ring_data):
    mock_label_ring_schema, mock_label_ring_response = mock_label_ring_data
    mock_process_label_ring.delay.return_value = AsyncMock(
        id=mock_label_ring_response.task_id
    )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/rings/label", json=mock_label_ring_schema.model_dump()
        )
        assert response.status_code == 202
        assert response.json() == mock_label_ring_response.model_dump()


@pytest.fixture()
def mock_annotation_ring_data():

    mock_annotation_ring_tmpdir = create_mock_session_directory(str(uuid.uuid4()))
    session_id = mock_annotation_ring_tmpdir.name

    mock_annotation_ring_schema = AnnotationRingSchema(
        reference=RingReference(session_id=session_id),
        tsv_id=create_mock_session_file(session_id=session_id).name,
    )

    mock_annotation_ring_response = AnnotationRingResponse(task_id="some_task_id")

    yield mock_annotation_ring_schema, mock_annotation_ring_response

    # Cleanup after tests deleting temporary session directory tree
    shutil.rmtree(mock_annotation_ring_tmpdir)


@pytest.mark.asyncio
@patch("brick.api.endpoints.rings.process_annotation_ring")
async def test_create_annotation_ring_success(
    mock_process_annotation_ring, mock_annotation_ring_data
):
    mock_annotation_ring_schema, mock_annotation_ring_response = (
        mock_annotation_ring_data
    )

    mock_process_annotation_ring.delay.return_value = AsyncMock(
        id=mock_annotation_ring_response.task_id
    )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/rings/annotation", json=mock_annotation_ring_schema.model_dump()
        )
        assert response.status_code == 202
        assert response.json() == mock_annotation_ring_response.model_dump()


@pytest.mark.asyncio
@patch("brick.api.endpoints.rings.process_annotation_ring")
async def test_create_annotation_ring_failure(
    mock_process_annotation_ring, mock_annotation_ring_data
):
    mock_annotation_ring_schema, _ = mock_annotation_ring_data
    mock_process_annotation_ring.delay.side_effect = Exception("Some error")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/rings/annotation", json=mock_annotation_ring_schema.model_dump()
        )
        assert response.status_code == 500


@pytest.fixture()
def mock_blast_ring_data():

    mock_blast_ring_tmpdir = create_mock_session_directory(str(uuid.uuid4()))
    session_id = mock_blast_ring_tmpdir.name

    mock_blast_ring_schema = BlastRingSchema(
        reference=RingReference(
            session_id=session_id,
            reference_id=create_mock_session_file(session_id=session_id).name,
        ),
        genome_id=create_mock_session_file(session_id=session_id).name,
    )

    mock_blast_ring_response = BlastRingResponse(task_id="some_task_id")

    yield mock_blast_ring_schema, mock_blast_ring_response

    # Cleanup after tests deleting temporary session directory tree
    shutil.rmtree(mock_blast_ring_tmpdir)


@pytest.mark.asyncio
@patch("brick.api.endpoints.rings.process_blast_ring")
async def test_create_blast_ring_success(mock_process_blast_ring, mock_blast_ring_data):
    mock_blast_ring_schema, mock_blast_ring_response = mock_blast_ring_data
    mock_process_blast_ring.delay.return_value = AsyncMock(
        id=mock_blast_ring_response.task_id
    )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/rings/blast", json=mock_blast_ring_schema.model_dump()
        )
        assert response.status_code == 202
        assert response.json() == mock_blast_ring_response.model_dump()


@pytest.mark.asyncio
@patch("brick.api.endpoints.rings.process_blast_ring")
async def test_create_blast_ring_failure(mock_process_blast_ring, mock_blast_ring_data):
    mock_blast_ring_schema, _ = mock_blast_ring_data
    mock_process_blast_ring.delay.side_effect = Exception("Some error")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/rings/blast", json=mock_blast_ring_schema.model_dump()
        )
        assert response.status_code == 500
