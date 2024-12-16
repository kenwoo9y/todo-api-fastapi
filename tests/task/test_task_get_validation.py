import pytest
import starlette.status


@pytest.mark.asyncio
async def test_get_task_by_invalid_id(async_client):
    # 無効なタスクID（例: 文字列）でユーザ取得
    response = await async_client.get("/tasks/invalid_id")
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
