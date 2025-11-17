import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI, HTTPException
from src.domain.models.order import Order
from src.infrastructure.inbound.api.routers.orders_router import get_orders_router

@pytest.fixture
def mock_service():
    return AsyncMock()

@pytest.fixture
def app_with_router(mock_service):
    app = FastAPI()
    router = get_orders_router(mock_service)
    app.include_router(router)
    return app, mock_service

@pytest.mark.asyncio
async def test_create_order_success(app_with_router):
    app, mock_service = app_with_router
    order_data = {"item": "Test Item", "quantity": 2}
    expected_order = Order(id=1, item="Test Item", quantity=2)
    mock_service.create.return_value = expected_order
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/orders", json=order_data)
        
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["item"] == "Test Item"
    assert response.json()["quantity"] == 2

@pytest.mark.asyncio
async def test_get_all_orders_success(app_with_router):
    app, mock_service = app_with_router
    expected_orders = [
        Order(id=1, item="Item1", quantity=1),
        Order(id=2, item="Item2", quantity=2)
    ]
    mock_service.get_all.return_value = expected_orders
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/orders")
        
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_get_order_by_id_success(app_with_router):
    app, mock_service = app_with_router
    expected_order = Order(id=1, item="Test Item", quantity=1)
    mock_service.get_by_id.return_value = expected_order
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/orders/1")
        
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.asyncio
async def test_get_order_by_id_not_found(app_with_router):
    app, mock_service = app_with_router
    mock_service.get_by_id.return_value = None
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/orders/999")
        
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"

@pytest.mark.asyncio
async def test_update_order_success(app_with_router):
    app, mock_service = app_with_router
    order_data = {"item": "Updated Item", "quantity": 3}
    expected_order = Order(id=1, item="Updated Item", quantity=3)
    mock_service.update.return_value = expected_order
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.patch("/orders/1", json=order_data)
        
    assert response.status_code == 200
    assert response.json()["item"] == "Updated Item"

@pytest.mark.asyncio
async def test_update_order_not_found(app_with_router):
    app, mock_service = app_with_router
    order_data = {"item": "Updated Item", "quantity": 3}
    mock_service.update.return_value = None
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.patch("/orders/999", json=order_data)
        
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_order_success(app_with_router):
    app, mock_service = app_with_router
    mock_service.delete.return_value = True
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete("/orders/1")
        
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_delete_order_not_found(app_with_router):
    app, mock_service = app_with_router
    mock_service.delete.return_value = False
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete("/orders/999")
        
    assert response.status_code == 404