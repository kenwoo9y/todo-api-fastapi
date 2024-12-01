import pytest
import starlette.status


@pytest.mark.asyncio
async def test_create_user_ok(async_client):
    # ユーザー作成の正常系テスト
    payload = {
        "username": "foobar",
        "email": "foobar@example.com",
        "first_name": "Foo",
        "last_name": "Bar",
    }
    response = await async_client.post("/users", json=payload)

    # ステータスコードとレスポンスデータの確認
    assert response.status_code == starlette.status.HTTP_201_CREATED
    response_obj = response.json()
    assert response_obj["username"] == payload["username"]
    assert response_obj["email"] == payload["email"]
    assert response_obj["first_name"] == payload["first_name"]
    assert response_obj["last_name"] == payload["last_name"]
    assert "created_at" in response_obj
    assert "updated_at" in response_obj


@pytest.mark.asyncio
async def test_create_user_duplicate_username(async_client):
    # 初回のユーザー作成
    payload = {
        "username": "duplicateuser",
        "email": "unique@example.com",
        "first_name": "Unique",
        "last_name": "User",
    }
    response = await async_client.post("/users", json=payload)
    assert response.status_code == starlette.status.HTTP_201_CREATED

    # 同じ username で再度作成
    payload["email"] = "another@example.com"  # 別のメールアドレスを指定
    response = await async_client.post("/users", json=payload)

    # ステータスコードの確認
    assert response.status_code == starlette.status.HTTP_409_CONFLICT

    # エラーメッセージの確認
    response_obj = response.json()
    assert response_obj["detail"] == "Username already exists"
