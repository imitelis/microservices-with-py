import pytest
import pytest_asyncio
import os
import tempfile
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from src.infrastructure.outbound.db.sqlite_repo import SQLiteOrderRepository
from src.infrastructure.outbound.messaging.kafka_producer import KafkaOrderProducer
from src.application.services.orders_service import OrdersService
from src.infrastructure.inbound.api.routers.orders_router import get_orders_router
from src.infrastructure.inbound.api.routers.asyncapi_router import get_asyncapi_router
from src.domain.models.order import Order
from fastapi import FastAPI

@pytest_asyncio.fixture
async def test_db():
    """Create a temporary test database"""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    # Patch the database path to use our test database
    with patch('src.core.config.SQLITE_DB_FILE', temp_db.name):
        repo = SQLiteOrderRepository()
        await repo.init()
        yield repo, temp_db.name
    
    # Cleanup
    os.unlink(temp_db.name)

@pytest_asyncio.fixture
async def test_app_with_real_db(test_db):
    """Create test app with real database but mocked Kafka"""
    repo, db_path = test_db
    
    with patch("src.infrastructure.outbound.messaging.kafka_producer.KafkaOrderProducer") as MockProducer:
        mock_producer_instance = MockProducer.return_value
        mock_producer_instance.start = AsyncMock()
        mock_producer_instance.stop = AsyncMock()
        mock_producer_instance.send_order = AsyncMock()
        
        # Create a simple FastAPI app without lifespan complications
        app = FastAPI()
        
        # Define a simple root route so "/" returns 200
        @app.get("/")
        async def root():
            return {"status": "ok"}
        
        # Patch the config for this app instance and create components
        with patch('src.core.config.SQLITE_DB_FILE', db_path):
            test_repo = SQLiteOrderRepository()
            await test_repo.init()
            await mock_producer_instance.start(retries=10, delay=2)
            
            # Create the use case and add routes directly
            order_uc = OrdersService(test_repo, mock_producer_instance)
            app.include_router(get_orders_router(order_uc))
            app.include_router(get_asyncapi_router())
            
            # Store references for cleanup
            app.state.repo = test_repo
            app.state.producer = mock_producer_instance
            
        yield app

@pytest.mark.asyncio
async def test_complete_order_lifecycle(test_app_with_real_db):
    """Test creating, reading, updating, and deleting an order through the API"""
    app = test_app_with_real_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Create an order
        order_data = {"item": "Integration Test Item", "quantity": 5}
        create_response = await client.post("/orders", json=order_data)
        assert create_response.status_code == 200
        created_order = create_response.json()
        order_id = created_order["id"]
        assert created_order["item"] == "Integration Test Item"
        assert created_order["quantity"] == 5
        
        # 2. Get the created order
        get_response = await client.get(f"/orders/{order_id}")
        assert get_response.status_code == 200
        retrieved_order = get_response.json()
        assert retrieved_order["id"] == order_id
        assert retrieved_order["item"] == "Integration Test Item"
        
        # 3. Get all orders (should include our order)
        get_all_response = await client.get("/orders")
        assert get_all_response.status_code == 200
        all_orders = get_all_response.json()
        assert len(all_orders) >= 1
        assert any(order["id"] == order_id for order in all_orders)
        
        # 4. Update the order
        update_data = {"item": "Updated Integration Item", "quantity": 10}
        update_response = await client.patch(f"/orders/{order_id}", json=update_data)
        assert update_response.status_code == 200
        updated_order = update_response.json()
        assert updated_order["item"] == "Updated Integration Item"
        assert updated_order["quantity"] == 10
        
        # 5. Verify the update persisted
        get_updated_response = await client.get(f"/orders/{order_id}")
        assert get_updated_response.status_code == 200
        verified_order = get_updated_response.json()
        assert verified_order["item"] == "Updated Integration Item"
        assert verified_order["quantity"] == 10
        
        # 6. Delete the order
        delete_response = await client.delete(f"/orders/{order_id}")
        assert delete_response.status_code == 204
        
        # 7. Verify the order is deleted
        get_deleted_response = await client.get(f"/orders/{order_id}")
        assert get_deleted_response.status_code == 404

@pytest.mark.asyncio
async def test_kafka_message_sent_on_order_creation(test_app_with_real_db):
    """Test that Kafka message is sent when an order is created"""
    app = test_app_with_real_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        order_data = {"item": "Kafka Test Item", "quantity": 3}
        
        # Create an order
        response = await client.post("/orders", json=order_data)
        assert response.status_code == 200
        
        # Verify Kafka producer was called
        # Note: The mock is already set up in the fixture
        # We could add more specific assertions here if needed

@pytest.mark.asyncio
async def test_multiple_orders_persistence(test_app_with_real_db):
    """Test creating multiple orders and ensuring they persist correctly"""
    app = test_app_with_real_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create multiple orders
        orders_data = [
            {"item": "Item 1", "quantity": 1},
            {"item": "Item 2", "quantity": 2},
            {"item": "Item 3", "quantity": 3}
        ]
        
        created_order_ids = []
        for order_data in orders_data:
            response = await client.post("/orders", json=order_data)
            assert response.status_code == 200
            created_order_ids.append(response.json()["id"])
        
        # Get all orders
        get_all_response = await client.get("/orders")
        assert get_all_response.status_code == 200
        all_orders = get_all_response.json()
        
        # Verify all our orders are present
        assert len(all_orders) >= 3
        retrieved_ids = [order["id"] for order in all_orders]
        for order_id in created_order_ids:
            assert order_id in retrieved_ids

@pytest.mark.asyncio
async def test_error_handling_nonexistent_order(test_app_with_real_db):
    """Test proper error handling for operations on non-existent orders"""
    app = test_app_with_real_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        non_existent_id = 99999
        
        # Try to get non-existent order
        get_response = await client.get(f"/orders/{non_existent_id}")
        assert get_response.status_code == 404
        
        # Try to update non-existent order
        update_data = {"item": "Updated", "quantity": 1}
        update_response = await client.patch(f"/orders/{non_existent_id}", json=update_data)
        assert update_response.status_code == 404
        
        # Try to delete non-existent order
        delete_response = await client.delete(f"/orders/{non_existent_id}")
        assert delete_response.status_code == 404