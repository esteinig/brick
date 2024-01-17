import pytest

from httpx import AsyncClient
from brick.api.main import app
from brick.api.models import Session
from unittest.mock import AsyncMock, patch


# Mock session data
mock_session_data = Session(
    id="some_uuid", date="some_iso_date", files=[], rings=[]
)

@pytest.fixture
def mock_motor_collection():
    # This mock represents the collection returned by get_session_collection_motor function
    mock_collection = AsyncMock()
    mock_collection.find_one.return_value = mock_session_data.model_dump()  # session query must be returned as dict
    return mock_collection

@patch('brick.api.endpoints.sessions.get_session_collection_motor')
@pytest.mark.asyncio
async def test_get_session_success(mock_get_session_collection_motor, mock_motor_collection):
    # Set the mock collection as the return value of the function
    mock_get_session_collection_motor.return_value = mock_motor_collection

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/sessions/some_uuid")
        assert response.status_code == 200
        assert response.json() == mock_session_data.model_dump() 

@patch('brick.api.endpoints.sessions.get_session_collection_motor')
@pytest.mark.asyncio
async def test_get_session_failure(mock_get_session_collection_motor, mock_motor_collection):
    # Set the mock collection as the return value of the function
    mock_get_session_collection_motor.return_value = mock_motor_collection
    # Set the return value to None to imitate no session model found 
    mock_get_session_collection_motor.return_value.find_one.return_value = None

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/sessions/none_existent_uuid")
        assert response.status_code == 404
        assert response.json()["detail"] == "Session not found"
