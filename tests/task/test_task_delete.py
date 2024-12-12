import pytest
import starlette.status


@pytest.mark.asyncio
async def test_delete_task_success(async_client):
    # テスト用データの作成
    payload = {
        "title": "foo",
        "description": "bar",
        "due_date": "2025-01-01",
        "status": "ToDo",
        "owner_id": 0,
    }
    create_response = await async_client.post("/tasks", json=payload)
    task_id = create_response.json()["id"]

    # タスク削除
    delete_response = await async_client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == starlette.status.HTTP_204_NO_CONTENT

    # 削除後に存在しないことを確認
    get_response = await async_client.get(f"/tasks/{task_id}")
    assert get_response.status_code == starlette.status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_task_invalid_id(async_client):
    # 存在しないタスクIDで削除を試行
    response = await async_client.delete("/tasks/99999")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Task not found"
