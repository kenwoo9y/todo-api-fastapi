import pytest
import starlette.status


@pytest.mark.asyncio
async def test_create_user_ok(async_client):
    #ユーザー作成の正常系テスト
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
