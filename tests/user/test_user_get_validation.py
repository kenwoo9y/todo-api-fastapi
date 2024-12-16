import pytest
import starlette.status


@pytest.mark.asyncio
async def test_get_user_by_invalid_id(async_client):
    # 無効なユーザーID（例: 文字列）でユーザ取得
    response = await async_client.get("/users/invalid_id")
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
