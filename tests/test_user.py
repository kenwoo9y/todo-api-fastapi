import pytest
import starlette.status


@pytest.mark.asyncio
async def test_create_user_ok(async_client):
    # リクエストデータ
    payload = {
        "username": "foobar",
        "email": "foobar@example.com",
        "first_name": "foo",
        "last_name": "bar",
    }

    # ユーザー作成APIへのPOSTリクエスト
    response = await async_client.post("/users", json=payload)

    # ステータスコードの確認
    assert response.status_code == starlette.status.HTTP_200_OK

    # レスポンスデータの確認
    response_obj = response.json()
    assert response_obj["username"] == payload["username"]
    assert response_obj["email"] == payload["email"]
    assert response_obj["first_name"] == payload["first_name"]
    assert response_obj["last_name"] == payload["last_name"]


@pytest.mark.asyncio
async def test_get_user_by_id(async_client):
    # 新規ユーザーの作成
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "test",
        "last_name": "user",
    }

    create_response = await async_client.post("/users", json=payload)
    user_id = create_response.json()["id"]

    # GETリクエストでユーザー取得
    response = await async_client.get(f"/users/{user_id}")
    assert response.status_code == starlette.status.HTTP_200_OK
    user_data = response.json()
    assert user_data["username"] == payload["username"]
    assert user_data["email"] == payload["email"]
