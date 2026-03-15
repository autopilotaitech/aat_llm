import os
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
async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "models_loaded" in data


@pytest.mark.asyncio
async def test_list_models(client):
    resp = await client.get("/api/tags")
    assert resp.status_code == 200
    data = resp.json()
    assert "models" in data
    assert isinstance(data["models"], list)


@pytest.mark.asyncio
async def test_generate_missing_model(client):
    resp = await client.post("/api/generate", json={
        "model": "nonexistent.gguf",
        "prompt": "hello",
    })
    assert resp.status_code == 404
    data = resp.json()
    assert "detail" in data or "error" in data


@pytest.mark.asyncio
async def test_delete_missing_model(client):
    resp = await client.request("DELETE", "/api/delete", json={
        "name": "nonexistent.gguf",
    })
    assert resp.status_code == 404
    data = resp.json()
    assert "detail" in data or "error" in data


@pytest.mark.asyncio
async def test_chat_missing_model(client):
    resp = await client.post("/api/chat", json={
        "model": "nonexistent.gguf",
        "messages": [{"role": "user", "content": "hi"}],
    })
    assert resp.status_code == 404
    data = resp.json()
    assert "detail" in data or "error" in data


def test_claude_md_exists():
    assert os.path.exists("CLAUDE.md")
    with open("CLAUDE.md", "r") as f:
        content = f.read()
    assert "aat_llm" in content
