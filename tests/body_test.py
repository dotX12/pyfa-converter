import datetime

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def tests_one(async_client: AsyncClient):

    data = {
        "title": "KEY1",
        "date": datetime.datetime.now().isoformat(),
        "amount": 10212.11,
        "unit_price": 12012.12,
    }
    files = {"document": (".gitignore", open(".gitignore", "rb"), "text/plain")}

    response_post = await async_client.post(
        url="/form-data-body",
        data=data,
        files=files,
    )

    assert response_post.status_code in [200, 201]
    assert response_post.json() == {
        "title": "KEY1",
        "date": "2022-09-13",
        "file_name": ".gitignore",
    }
