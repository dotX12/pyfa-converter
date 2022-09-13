import asyncio
from typing import Generator
from httpx import AsyncClient
import pytest_asyncio

from examples.main import app


@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop

    loop.close()


@pytest_asyncio.fixture(scope="module")
async def async_client() -> Generator:
    async with AsyncClient(
        app=app, base_url="http://testserver"
    ) as client_:
        yield client_
