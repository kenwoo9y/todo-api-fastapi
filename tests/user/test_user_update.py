import pytest
import starlette.status


@pytest.mark.asyncio
async def test_update_user_success(async_client):
    # テスト用データの作成
    payload = {
        "username": "foobar",
        "email": "foobar@example.com",
        "first_name": "Foo",
        "last_name": "Bar",
    }
    create_response = await async_client.post("/users", json=payload)
    user_id = create_response.json()["id"]

    # 更新データ
    update_payload = {
        "username": "buzqux",
        "email": "buzqux@example.com",
        "first_name": "Buz",
        "last_name": "Qux",
    }

    # ユーザー更新
    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_200_OK

    # 更新後のデータを確認
    updated_user = response.json()
    assert updated_user["username"] == update_payload["username"]
    assert updated_user["email"] == update_payload["email"]
    assert updated_user["first_name"] == update_payload["first_name"]
    assert updated_user["last_name"] == update_payload["last_name"]


@pytest.mark.asyncio
async def test_partial_update_user_success(async_client):
    # テスト用データの作成
    payload = {
        "username": "partialuser",
        "email": "partialuser@example.com",
        "first_name": "Partial",
        "last_name": "User",
    }
    create_response = await async_client.post("/users", json=payload)
    user_id = create_response.json()["id"]

    # 部分更新データ
    update_payload = {
        "first_name": "PartiallyUpdated",
    }

    # ユーザー更新
    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_200_OK

    # 更新後のデータを確認
    updated_user = response.json()
    assert updated_user["first_name"] == update_payload["first_name"]
    assert updated_user["last_name"] == payload["last_name"]  # 変更していないフィールド


@pytest.mark.asyncio
async def test_update_user_not_found(async_client):
    # 存在しないユーザーIDで更新
    update_payload = {
        "username": "nonexistentuser",
        "email": "nonexistentuser@example.com",
        "first_name": "NonExistent",
        "last_name": "User",
    }
    response = await async_client.patch("/users/99999", json=update_payload)
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_update_user_duplicate_username(async_client):
    # ユーザー1の作成
    user1 = {
        "username": "duplicateuser1",
        "email": "duplicate1@example.com",
        "first_name": "Duplicate",
        "last_name": "User1",
    }
    create_response1 = await async_client.post("/users", json=user1)
    user_id1 = create_response1.json()["id"]

    # ユーザー2の作成
    user2 = {
        "username": "duplicateuser2",
        "email": "duplicate2@example.com",
        "first_name": "Duplicate",
        "last_name": "User2",
    }
    await async_client.post("/users", json=user2)

    # ユーザー1のusernameをユーザー2のusernameに変更
    update_payload = {"username": user2["username"]}
    response = await async_client.patch(f"/users/{user_id1}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Username or Email already exists"


@pytest.mark.asyncio
async def test_update_user_duplicate_email(async_client):
    # ユーザー1の作成
    user1 = {
        "username": "duplicateuser1",
        "email": "duplicate1@example.com",
        "first_name": "Duplicate",
        "last_name": "User1",
    }
    create_response1 = await async_client.post("/users", json=user1)
    user_id1 = create_response1.json()["id"]

    # ユーザー2の作成
    user2 = {
        "username": "duplicateuser2",
        "email": "duplicate2@example.com",
        "first_name": "Duplicate",
        "last_name": "User2",
    }
    await async_client.post("/users", json=user2)

    # ユーザー1のemailをユーザー2のemailに変更
    update_payload = {"email": user2["email"]}
    response = await async_client.patch(f"/users/{user_id1}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Username or Email already exists"