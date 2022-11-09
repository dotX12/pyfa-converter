import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def tests_one(async_client: AsyncClient):
    params = {"id": 100, "title": "test", "data": [1, 2, 3, 4, 5]}

    response_post = await async_client.post(
        url="/test",
        data=params,
    )

    assert response_post.status_code in [200, 201]
    assert response_post.json() == {
        "data": {"id": 100, "title": "test", "data": [1, 2, 3, 4, 5]}
    }
