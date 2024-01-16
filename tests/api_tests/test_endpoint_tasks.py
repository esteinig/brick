from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from brick.api.main import app
from brick.api.schemas import TaskStatus, FileType, FileFormat, Selections
from brick.api.models import SessionFile

client = TestClient(app)

def mock_session_file():
    return SessionFile(
        session_id="some_uuid",  
        id="some_uuid", 
        type=FileType.GENOME, 
        format=FileFormat.FASTA, 
        records=100,
        total_length=200,
        name="file_name.ext",
        name_original="original_file_name.ext",
        selections=Selections()
    )

def create_mock_async_result(status: TaskStatus, ready: bool, success: bool, error_message: str):
    mock_result = MagicMock()
    mock_result.status = status.value
    mock_result.ready.return_value = ready
    if success:
        mock_result.get.return_value = {
            "success": success, 
            "result": mock_session_file().model_dump()
        }
    else:
        mock_result.get.return_value = {
            "success": success, 
            "error": error_message
        }
    return mock_result

@patch('brick.api.endpoints.tasks.AsyncResult')
def test_get_task_status(mock_async_result):
    mock_async_result.return_value = create_mock_async_result(
        TaskStatus.PENDING, True, True, ""
    )
    response = client.get("/tasks/status/test_task_id")
    assert response.status_code == 200  
    assert response.json() == {"task_id": "test_task_id", "status": TaskStatus.PENDING.value}

@patch('brick.api.endpoints.tasks.AsyncResult')
def test_get_task_result_not_ready(mock_async_result):
    mock_async_result.return_value = create_mock_async_result(
        TaskStatus.PROCESSING, False, True, ""
    )
    response = client.get("/tasks/result/test_task_id")
    assert response.status_code == 202
    assert response.json()["status"] == TaskStatus.PROCESSING.value

@patch('brick.api.endpoints.tasks.AsyncResult')
def test_get_task_result_success(mock_async_result):
    mock_async_result.return_value = create_mock_async_result(
        TaskStatus.SUCCESS, True, True, ""
        )
    response = client.get("/tasks/result/test_task_id")
    assert response.status_code == 200
    assert response.json()["status"] == TaskStatus.SUCCESS.value

@patch('brick.api.endpoints.tasks.AsyncResult')
def test_get_task_result_failure(mock_async_result):
    error_message = "error_message"
    mock_async_result.return_value = create_mock_async_result(
        TaskStatus.FAILURE, True, False, error_message
    )
    response = client.get("/tasks/result/test_task_id")
    assert response.status_code == 500
    assert response.json()["detail"] == error_message
