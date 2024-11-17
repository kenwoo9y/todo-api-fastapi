import pytest
import starlette.status

@pytest.mark.asyncio
async def test_create_user_ok(async_client):
    # リクエストデータ
    payload = {
        "user_name": "foobar",
        "email": "foobar@example.com",
        "first_name": "foo",
        "last_name": "bar",
        "password": "password"
    }

    # ユーザー作成APIへのPOSTリクエスト
    response = await async_client.post("/users", json=payload)
    
    # ステータスコードの確認
    assert response.status_code == starlette.status.HTTP_200_OK
    
    # レスポンスデータの確認
    response_obj = response.json()
    assert response_obj["user_name"] == payload["user_name"]
    assert response_obj["email"] == payload["email"]
    assert response_obj["first_name"] == payload["first_name"]
    assert response_obj["last_name"] == payload["last_name"]