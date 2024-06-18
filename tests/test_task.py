import pytest
import starlette.status

@pytest.mark.asyncio
async def test_create_task_ok(async_client):
    response = await async_client.post("/tasks", json={
        "title": "テストタスク",
        "description": "テストタスク",
        "due_date": "2024-01-01",
        "status": "ToDo",
        "owner_id": "9999"
    })
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "テストタスク"