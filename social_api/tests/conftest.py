import os
from typing import AsyncGenerator, Generator
import pytest
from unittest.mock import AsyncMock, Mock
from fastapi.testclient import TestClient
from httpx import AsyncClient, Request, Response
from social_api.tests.helpers import create_post

os.environ["ENV_STATE"] = "test"
from social_api.database import database, user_table
from social_api.main import app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield database
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        yield ac


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@example.net", "password": "1234"}
    await async_client.post("/register", json=user_details)
    query = user_table.select().where(user_table.c.email == user_details["email"])
    user = await database.fetch_one(query)
    user_details["id"] = user.id
    return user_details


@pytest.fixture()
async def confirmed_user(registered_user: dict) -> dict:
    query = (
        user_table.update().where(
            user_table.c.email == registered_user["email"],
        )
    ).values(confirmed=True)
    await database.execute(query)
    return registered_user


@pytest.fixture()
async def logged_in_token(async_client: AsyncClient, confirmed_user: dict) -> str:
    response = await async_client.post("/token", json=confirmed_user)
    return response.json()["access_token"]


@pytest.fixture(autouse=True)
def mock_httpx_client(mocker):
    mocked_client = mocker.patch("social_api.tasks.httpx.AsyncClient")

    mocked_async_clint = Mock()
    response = Response(status_code=200, content="", request=Request("POST", "//"))
    mocked_async_clint.post = AsyncMock(return_value=response)
    mocked_client.return_value.__aenter__.return_value = mocked_async_clint

    return mocked_async_clint


@pytest.fixture()
async def created_post(async_client: AsyncClient, logged_in_token: str) -> dict:
    return await create_post("Test Post", async_client, logged_in_token)
