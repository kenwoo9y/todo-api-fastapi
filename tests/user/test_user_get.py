import pytest
import starlette.status


@pytest.mark.asyncio
async def test_get_user_by_id_success(async_client):
    # テスト用データの作成
    payload = {
        "username": "foobar",
        "email": "foobar@example.com",
        "first_name": "Foo",
        "last_name": "Bar",
    }
    create_response = await async_client.post("/users", json=payload)
    user_id = create_response.json()["id"]

    # ユーザー取得
    response = await async_client.get(f"/users/{user_id}")
    assert response.status_code == starlette.status.HTTP_200_OK
    user_data = response.json()
    assert user_data["username"] == payload["username"]
    assert user_data["email"] == payload["email"]
    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert "created_at" in user_data
    assert "updated_at" in user_data


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(async_client):
    # 存在しないIDを取得
    response = await async_client.get("/users/99999")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_get_user_by_username_success(async_client):
    # テスト用データの作成
    payload = {
        "username": "foobar",
        "email": "foobar@example.com",
        "first_name": "Foo",
        "last_name": "Bar",
    }
    await async_client.post("/users", json=payload)

    # ユーザー名で取得
    response = await async_client.get("/users/username/foobar")
    assert response.status_code == starlette.status.HTTP_200_OK
    user_data = response.json()
    assert user_data["username"] == payload["username"]
    assert user_data["email"] == payload["email"]
    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert "created_at" in user_data
    assert "updated_at" in user_data


@pytest.mark.asyncio
async def test_get_user_by_username_not_found(async_client):
    # 存在しないユーザー名を取得
    response = await async_client.get("/users/username/unknownuser")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_get_all_users(async_client):
    # 複数ユーザーを作成
    user1 = {
        "username": "user1",
        "email": "user1@example.com",
        "first_name": "First1",
        "last_name": "Last1",
    }
    user2 = {
        "username": "user2",
        "email": "user2@example.com",
        "first_name": "First2",
        "last_name": "Last2",
    }
    await async_client.post("/users", json=user1)
    await async_client.post("/users", json=user2)

    # 全ユーザー取得
    response = await async_client.get("/users")
    assert response.status_code == starlette.status.HTTP_200_OK
    users = response.json()
    assert len(users) >= 2  # 他のテストで作成したユーザーも含まれる可能性あり
    usernames = [user["username"] for user in users]
    assert "user1" in usernames
    assert "user2" in usernames
