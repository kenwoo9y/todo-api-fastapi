import pytest
import starlette.status


@pytest.mark.asyncio
async def test_get_task_by_id_success(async_client):
    # テスト用データの作成
    payload = {
        "title": "test task",
        "description": "task description",
        "due_date": "2025-01-01",
        "status": "ToDo",
        "owner_id": 0,
    }
    create_response = await async_client.post("/tasks", json=payload)
    task_id = create_response.json()["id"]

    # タスク取得
    response = await async_client.get(f"/tasks/{task_id}")
    assert response.status_code == starlette.status.HTTP_200_OK
    task_data = response.json()
    assert task_data["title"] == payload["title"]
    assert task_data["description"] == payload["description"]
    assert task_data["due_date"] == payload["due_date"]
    assert task_data["status"] == payload["status"]
    assert task_data["owner_id"] == payload["owner_id"]
    assert "created_at" in task_data
    assert "updated_at" in task_data


@pytest.mark.asyncio
async def test_get_task_by_invalid_id(async_client):
    # 存在しないIDを取得
    response = await async_client.get("/tasks/99999")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Task not found"


@pytest.mark.asyncio
async def test_get_all_tasks(async_client):
    # 複数タスクを作成
    task1 = {
        "title": "task1",
        "description": "task1 description",
        "due_date": "2025-01-01",
        "status": "ToDo",
        "owner_id": 0,
    }
    task2 = {
        "title": "task2",
        "description": "task2 description",
        "due_date": "2025-01-01",
        "status": "ToDo",
        "owner_id": 0,
    }
    await async_client.post("/tasks", json=task1)
    await async_client.post("/tasks", json=task2)

    # 全タスク取得
    response = await async_client.get("/tasks")
    assert response.status_code == starlette.status.HTTP_200_OK
    tasks = response.json()
    assert len(tasks) >= 2  # 他のテストで作成したタスクも含まれる可能性あり
    titles = [task["title"] for task in tasks]
    assert "task1" in titles
    assert "task2" in titles
