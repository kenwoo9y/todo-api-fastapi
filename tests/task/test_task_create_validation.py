import pytest
import starlette.status


@pytest.mark.asyncio
async def test_create_task_missing_title(async_client):
    # タイトルが欠けたリクエスト
    payload = {
        "description": "task description",
        "due_date": "2025-01-01",
        "status": "ToDo",
        "owner_id": 0,
    }
    response = await async_client.post("/tasks", json=payload)

    # タイトルのバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "title" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_create_task_max_length_title(async_client):
    # タイトルが最大長の場合のリクエスト
    payload = {
        "title": "a" * 30,
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


@pytest.mark.asyncio
async def test_create_task_long_title(async_client):
    # タイトルが長すぎる場合のリクエスト
    payload = {
        "title": "a" * 31,
        "description": "task description",
        "due_date": "2025-01-01",
        "status": "ToDo",
        "owner_id": 0,
    }
    response = await async_client.post("/tasks", json=payload)

    # タイトルのバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "title" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_create_task_max_length_description(async_client):
    # descriptionが最大長の場合のリクエスト
    payload = {
        "title": "test task",
        "description": "a" * 255,
        "due_date": "2025-01-01",
        "status": "ToDo",
        "owner_id": 0,
    }
    response = await async_client.post("/tasks", json=payload)

    # ステータスコードとレスポンスデータの確認
    assert response.status_code == starlette.status.HTTP_201_CREATED
    response_obj = response.json()
    assert response_obj["description"] == payload["description"]


@pytest.mark.asyncio
async def test_create_task_long_description(async_client):
    # descriptionが長すぎる場合のリクエスト
    payload = {
        "title": "test task",
        "description": "a" * 256,
        "due_date": "2025-01-01",
        "status": "ToDo",
        "owner_id": 0,
    }
    response = await async_client.post("/tasks", json=payload)

    # descriptionのバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "description" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_create_task_invalid_due_date(async_client):
    # 不正なdue_date場合のリクエスト
    payload = {
        "title": "test task",
        "description": "task description",
        "due_date": "20250101",
        "status": "ToDo",
        "owner_id": 0,
    }
    response = await async_client.post("/tasks", json=payload)

    # due_dateのバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "due_date" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_create_task_invalid_status(async_client):
    # 不正なdue_date場合のリクエスト
    payload = {
        "title": "test task",
        "description": "task description",
        "due_date": "2025-01-01",
        "status": "FooBar",
        "owner_id": 0,
    }
    response = await async_client.post("/tasks", json=payload)

    # statusのバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "status" in response.json()["detail"][0]["loc"]
