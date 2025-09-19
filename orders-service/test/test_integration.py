import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_order_api():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/orders", json={"item": "Mouse", "quantity": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["item"] == "Mouse"
