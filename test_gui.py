import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from server import app


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_ui_served(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers.get("content-type", "")


@pytest.mark.asyncio
async def test_ui_has_chat_element(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert "chat-history" in resp.text


@pytest.mark.asyncio
async def test_pull_endpoint_exists(client):
    resp = await client.post("/api/pull", json={
        "repo_id": "test/test",
        "filename": "test.gguf",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
