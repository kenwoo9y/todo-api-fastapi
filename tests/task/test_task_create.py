import pytest
import starlette.status


@pytest.mark.asyncio
async def test_create_task_success(async_client):
    # タスク作成の正常系テスト
    payload = {
        "title": "test task",
        "description": "task description",
        "due_date": "2025-01-01",
        "status": "ToDo",
        "owner_id": 0,
    }
    response = await async_client.post("/tasks", json=payload)

    # ステータスコードとレスポンスデータの確認
    assert response.status_code == starlette.status.HTTP_201_CREATED
    response_obj = response.json()
    assert response_obj["title"] == payload["title"]
    assert response_obj["description"] == payload["description"]
    assert response_obj["due_date"] == payload["due_date"]
    assert response_obj["status"] == payload["status"]
    assert response_obj["owner_id"] == payload["owner_id"]
    assert "created_at" in response_obj
    assert "updated_at" in response_obj
