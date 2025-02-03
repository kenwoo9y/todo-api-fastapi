import pytest
import starlette.status


@pytest.mark.asyncio
async def test_update_task_invalid_id(async_client):
    # 更新データ
    update_payload = {
        "title": "baz",
        "description": "qux",
        "due_date": "2025-01-02",
        "status": "Doing",
        "owner_id": 999,
    }

    # 無効なタスクID（例: 文字列）でユーザ更新
    response = await async_client.patch("/tasks/invalid_id", json=update_payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update_task_empty_title(async_client):
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
    update_payload = {"title": ""}

    # タスク更新
    response = await async_client.patch(f"/tasks/{task_id}", json=update_payload)

    # タイトルのバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "title" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_update_task_max_length_title(async_client):
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
        "title": "a" * 30,
    }

    # タスク更新
    response = await async_client.patch(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_200_OK

    # 更新後のデータを確認
    updated_user = response.json()
    assert updated_user["title"] == update_payload["title"]
    # 変更していないフィールド
    assert updated_user["description"] == payload["description"]
    assert updated_user["due_date"] == payload["due_date"]
    assert updated_user["status"] == payload["status"]
    assert updated_user["owner_id"] == payload["owner_id"]


@pytest.mark.asyncio
async def test_update_task_long_title(async_client):
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
        "title": "a" * 31,
    }

    # タスク更新
    response = await async_client.patch(f"/tasks/{task_id}", json=update_payload)

    # タイトルのバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "title" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_update_task_max_length_description(async_client):
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
        "description": "a" * 255,
    }

    # タスク更新
    response = await async_client.patch(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_200_OK

    # 更新後のデータを確認
    updated_user = response.json()
    assert updated_user["description"] == update_payload["description"]
    # 変更していないフィールド
    assert updated_user["title"] == payload["title"]
    assert updated_user["due_date"] == payload["due_date"]
    assert updated_user["status"] == payload["status"]
    assert updated_user["owner_id"] == payload["owner_id"]


@pytest.mark.asyncio
async def test_update_task_long_description(async_client):
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
        "description": "a" * 256,
    }

    # タスク更新
    response = await async_client.patch(f"/tasks/{task_id}", json=update_payload)

    # タイトルのバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "description" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_update_task_invalid_due_date(async_client):
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
        "due_date": "20250101",
    }

    # タスク更新
    response = await async_client.patch(f"/tasks/{task_id}", json=update_payload)

    # due_dateのバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "due_date" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_update_task_invalid_status(async_client):
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
        "status": "FooBar",
    }

    # タスク更新
    response = await async_client.patch(f"/tasks/{task_id}", json=update_payload)

    # statusのバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "status" in response.json()["detail"][0]["loc"]
