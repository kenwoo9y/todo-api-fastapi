import pytest
import starlette.status


@pytest.mark.asyncio
async def test_update_user_invalid_id(async_client):
    # 更新データ
    update_payload = {
        "username": "buzqux",
        "email": "buzqux@example.com",
        "first_name": "Buz",
        "last_name": "Qux",
    }

    # 無効なユーザーID（例: 文字列）でユーザ更新
    response = await async_client.patch("/users/invalid_id", json=update_payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update_user_empty_username(async_client):
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
        "username": "",
    }

    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "username" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_update_user_max_length_username(async_client):
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
        "username": "a" * 30,  # 30文字
    }

    # ユーザー更新
    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_200_OK

    # 更新後のデータを確認
    updated_user = response.json()
    assert updated_user["username"] == update_payload["username"]
    # 変更していないフィールド
    assert updated_user["email"] == payload["email"]
    assert updated_user["first_name"] == payload["first_name"]
    assert updated_user["last_name"] == payload["last_name"]


@pytest.mark.asyncio
async def test_update_user_long_username(async_client):
    # テスト用データの作成
    payload = {
        "username": "foobar",
        "email": "foobar@example.com",
        "first_name": "Foo",
        "last_name": "Bar",
    }
    create_response = await async_client.post("/users", json=payload)
    user_id = create_response.json()["id"]

    # 更新データ(ユーザー名が長すぎる)
    update_payload = {
        "username": "a" * 31,  # 31文字
    }

    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "username" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_update_user_min_length_username(async_client):
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
        "username": "a" * 3,  # 3文字
    }

    # ユーザー更新
    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_200_OK

    # 更新後のデータを確認
    updated_user = response.json()
    assert updated_user["username"] == update_payload["username"]
    # 変更していないフィールド
    assert updated_user["email"] == payload["email"]
    assert updated_user["first_name"] == payload["first_name"]
    assert updated_user["last_name"] == payload["last_name"]


@pytest.mark.asyncio
async def test_update_user_short_username(async_client):
    # テスト用データの作成
    payload = {
        "username": "foobar",
        "email": "foobar@example.com",
        "first_name": "Foo",
        "last_name": "Bar",
    }
    create_response = await async_client.post("/users", json=payload)
    user_id = create_response.json()["id"]

    # 更新データ(ユーザー名が短かすぎる)
    update_payload = {
        "username": "a" * 2,  # 2文字
    }

    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "username" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_update_user_empty_email(async_client):
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
        "email": "",
    }

    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "email" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_update_user_invalid_email(async_client):
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
        "email": "invalid-email",
    }

    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "email" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_update_user_max_length_email(async_client):
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
        "email": "a" * 64 + "@example.com",  # ローカルパート64文字
    }

    # ユーザー更新
    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_200_OK

    # 更新後のデータを確認
    updated_user = response.json()
    assert updated_user["email"] == update_payload["email"]
    # 変更していないフィールド
    assert updated_user["username"] == payload["username"]
    assert updated_user["first_name"] == payload["first_name"]
    assert updated_user["last_name"] == payload["last_name"]


@pytest.mark.asyncio
async def test_update_user_long_email(async_client):
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
        "email": "a" * 65 + "@example.com",  # ローカルパート65文字
    }

    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "email" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_update_user_empty_first_name_and_last_name(async_client):
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
        "first_name": "",
        "last_name": "",
    }

    # ユーザー更新
    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_200_OK

    # 更新後のデータを確認
    updated_user = response.json()
    assert updated_user["first_name"] == ""
    assert updated_user["first_name"] == ""
    # 変更していないフィールド
    assert updated_user["username"] == payload["username"]
    assert updated_user["email"] == payload["email"]


@pytest.mark.asyncio
async def test_update_user_max_length_first_name(async_client):
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
        "first_name": "a" * 40,  # 40文字
    }

    # ユーザー更新
    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_200_OK

    # 更新後のデータを確認
    updated_user = response.json()
    assert updated_user["first_name"] == update_payload["first_name"]
    # 変更していないフィールド
    assert updated_user["username"] == payload["username"]
    assert updated_user["email"] == payload["email"]
    assert updated_user["last_name"] == payload["last_name"]


@pytest.mark.asyncio
async def test_update_user_long_first_name(async_client):
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
        "first_name": "a" * 41,  # 41文字
    }

    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "first_name" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_update_user_max_length_last_name(async_client):
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
        "last_name": "a" * 40,  # 40文字
    }

    # ユーザー更新
    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_200_OK

    # 更新後のデータを確認
    updated_user = response.json()
    assert updated_user["last_name"] == update_payload["last_name"]
    # 変更していないフィールド
    assert updated_user["username"] == payload["username"]
    assert updated_user["email"] == payload["email"]
    assert updated_user["first_name"] == payload["first_name"]


@pytest.mark.asyncio
async def test_update_user_long_last_name(async_client):
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
        "last_name": "a" * 41,  # 41文字
    }

    response = await async_client.patch(f"/users/{user_id}", json=update_payload)
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "last_name" in response.json()["detail"][0]["loc"]
