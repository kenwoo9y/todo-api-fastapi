import pytest
import starlette.status


@pytest.mark.asyncio
async def test_create_user_missing_username(async_client):
    # ユーザー名が欠けたリクエスト
    payload = {
        "email": "foobar@example.com",
        "first_name": "Foo",
        "last_name": "Bar",
    }
    response = await async_client.post("/users", json=payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "username" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_create_user_missing_email(async_client):
    # メールアドレスが欠けたリクエスト
    payload = {
        "username": "foobar",
        "first_name": "Foo",
        "last_name": "Bar"
    }
    response = await async_client.post("/users", json=payload)

    # バリデーションエラー（Email is required）を確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "email" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_create_user_invalid_email(async_client):
    # 無効なメールアドレスでリクエスト
    payload = {"username": "foobar", "email": "invalid-email", "first_name": "Foo", "last_name": "Bar"}
    response = await async_client.post("/users", json=payload)

    # メールアドレスのバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "email" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_create_user_long_username(async_client):
    # ユーザー名が長すぎる場合のリクエスト
    payload = {
        "username": "a" * 31,  # 31文字
        "email": "foobar@example.com",
        "first_name": "Foo",
        "last_name": "Bar",
    }
    response = await async_client.post("/users", json=payload)

    # ユーザー名のバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "username" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_create_user_empty_first_name_and_last_name(async_client):
    # First Name と Last Name が空でも許容される
    payload = {"username": "foobar", "email": "foobar@example.com", "first_name": "", "last_name": ""}
    response = await async_client.post("/users", json=payload)

    # ステータスコードは201 Createdとなり、first_name と last_name は空で返される
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == ""
    assert data["last_name"] == ""
