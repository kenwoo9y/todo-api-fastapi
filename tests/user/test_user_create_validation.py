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
async def test_create_user_max_length_username(async_client):
    # ユーザー名が最大長のリクエスト（正常ケース）
    payload = {
        "username": "a" * 30,  # 30文字
        "email": "foobar@example.com",
        "first_name": "Foo",
        "last_name": "Bar",
    }
    response = await async_client.post("/users", json=payload)

    # ユーザー名のバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_201_CREATED
    assert response.json()["username"] == payload["username"]


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
async def test_create_user_min_length_username(async_client):
    # ユーザー名が最小長のリクエスト（正常ケース）
    payload = {
        "username": "a" * 3,  # 3文字
        "email": "foobar@example.com",
        "first_name": "Foo",
        "last_name": "Bar",
    }
    response = await async_client.post("/users", json=payload)

    # ユーザー名のバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_201_CREATED
    assert response.json()["username"] == payload["username"]


@pytest.mark.asyncio
async def test_create_user_short_username(async_client):
    # ユーザー名が短ぎる場合のリクエスト
    payload = {
        "username": "a" * 2,  # 2文字
        "email": "foobar@example.com",
        "first_name": "Foo",
        "last_name": "Bar",
    }
    response = await async_client.post("/users", json=payload)

    # ユーザー名のバリデーションエラーを確認
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "username" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_create_user_missing_email(async_client):
    # メールアドレスが欠けたリクエスト
    payload = {"username": "foobar", "first_name": "Foo", "last_name": "Bar"}
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
async def test_create_user_max_length_email(async_client):
    # ローカルパート64文字のメールアドレス（正常ケース）
    payload = {
        "username": "foobar",
        "email": "a" * 64 + "@example.com",  # ローカルパート64文字
        "first_name": "Foo",
        "last_name": "Bar",
    }
    response = await async_client.post("/users", json=payload)
    assert response.status_code == starlette.status.HTTP_201_CREATED
    assert response.json()["email"] == payload["email"]


@pytest.mark.asyncio
async def test_create_user_long_email(async_client):
    # 長すぎるメールアドレス
    payload = {
        "username": "foobar",
        "email": "a" * 65 + "@example.com",  # ローカルパート65文字
        "first_name": "Foo",
        "last_name": "Bar",
    }
    response = await async_client.post("/users", json=payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "email" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_create_user_empty_first_name_and_last_name(async_client):
    # First Name と Last Name が空でも許容される
    payload = {"username": "foobar", "email": "foobar@example.com", "first_name": "", "last_name": ""}
    response = await async_client.post("/users", json=payload)

    # ステータスコードは201 Createdとなり、first_name と last_name は空で返される
    assert response.status_code == starlette.status.HTTP_201_CREATED
    data = response.json()
    assert data["first_name"] == ""
    assert data["last_name"] == ""


@pytest.mark.asyncio
async def test_create_user_max_length_first_name(async_client):
    # First Nameが最大長のリクエスト（正常ケース）
    payload = {"username": "foobar", "email": "foobar@example.com", "first_name": "a" * 40, "last_name": ""}
    response = await async_client.post("/users", json=payload)
    assert response.status_code == starlette.status.HTTP_201_CREATED
    assert response.json()["first_name"] == payload["first_name"]


@pytest.mark.asyncio
async def test_create_user_long_first_name(async_client):
    # 長すぎるFirst Name
    payload = {"username": "foobar", "email": "foobar@example.com", "first_name": "a" * 41, "last_name": ""}
    response = await async_client.post("/users", json=payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "first_name" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_create_user_max_length_last_name(async_client):
    # Last Nameが最大長のリクエスト（正常ケース）
    payload = {"username": "foobar", "email": "foobar@example.com", "first_name": "", "last_name": "a" * 40}
    response = await async_client.post("/users", json=payload)
    assert response.status_code == starlette.status.HTTP_201_CREATED
    assert response.json()["last_name"] == payload["last_name"]


@pytest.mark.asyncio
async def test_create_user_long_last_name(async_client):
    # 長すぎるLast Name
    payload = {"username": "foobar", "email": "foobar@example.com", "first_name": "", "last_name": "a" * 41}
    response = await async_client.post("/users", json=payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "last_name" in response.json()["detail"][0]["loc"]
