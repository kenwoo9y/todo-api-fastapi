import pytest
import starlette.status


@pytest.mark.asyncio
async def test_delete_user_success(async_client):
    # テスト用データの作成
    payload = {
        "username": "deletetestuser",
        "email": "deletetestuser@example.com",
        "first_name": "Delete",
        "last_name": "User",
    }
    create_response = await async_client.post("/users", json=payload)
    user_id = create_response.json()["id"]

    # ユーザー削除
    delete_response = await async_client.delete(f"/users/{user_id}")
    assert delete_response.status_code == starlette.status.HTTP_204_NO_CONTENT

    # 削除後に存在しないことを確認
    get_response = await async_client.get(f"/users/{user_id}")
    assert get_response.status_code == starlette.status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_user_not_found(async_client):
    # 存在しないユーザーIDで削除を試行
    response = await async_client.delete("/users/99999")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"
