import pytest
import starlette.status


@pytest.mark.asyncio
async def test_update_task_success(async_client):
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

    # 更新データ
    update_payload = {
        "title": "baz",
        "description": "qux",
        "due_date": "2025-01-02",
        "status": "Doing",
        "owner_id": 999,
    }

    # タスク更新
    response = await async_client.patch(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_200_OK

    # 更新後のデータを確認
    updated_user = response.json()
    assert updated_user["title"] == update_payload["title"]
    assert updated_user["description"] == update_payload["description"]
    assert updated_user["due_date"] == update_payload["due_date"]
    assert updated_user["status"] == update_payload["status"]
    assert updated_user["owner_id"] == update_payload["owner_id"]


@pytest.mark.asyncio
async def test_partial_update_task_success(async_client):
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

    # 更新データ
    update_payload = {
        "status": "Done",
    }

    # タスク更新
    response = await async_client.patch(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_200_OK

    # 更新後のデータを確認
    updated_user = response.json()
    assert updated_user["status"] == update_payload["status"]
    # 変更していないフィールド
    assert updated_user["title"] == payload["title"]
    assert updated_user["description"] == payload["description"]
    assert updated_user["due_date"] == payload["due_date"]
    assert updated_user["owner_id"] == payload["owner_id"]


@pytest.mark.asyncio
async def test_update_user_not_found(async_client):
    # テスト用データの作成
    payload = {
        "title": "foo",
        "description": "bar",
        "due_date": "2025-01-01",
        "status": "ToDo",
        "owner_id": 0,
    }
    await async_client.post("/tasks", json=payload)

    # 存在しないユーザーIDで更新
    update_payload = {
        "title": "baz",
        "description": "qux",
        "due_date": "2025-01-02",
        "status": "Doing",
        "owner_id": 999,
    }

    response = await async_client.patch("/tasks/99999", json=update_payload)
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Task not found"
