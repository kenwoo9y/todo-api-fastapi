import pytest
import starlette.status

@pytest.mark.asyncio
async def test_create_user_ok(async_client):
    response = await async_client.post("/users", json={
        "user_name": "foobar",
        "email": "foobar@example.com",
        "first_name": "foo",
        "last_name": "bar"
    })
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["user_name"] == "foobar" 