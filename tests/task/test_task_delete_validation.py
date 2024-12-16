import pytest
import starlette.status


@pytest.mark.asyncio
async def test_delete_task_invalid_id(async_client):
    # 無効なタスクID（例: 文字列）でユーザ削除
    response = await async_client.delete("/tasks/invalid_id")
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
