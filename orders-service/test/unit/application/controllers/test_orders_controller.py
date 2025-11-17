import pytest
from unittest.mock import AsyncMock
from src.application.controllers.orders_controller import OrdersController
from src.domain.models.order import Order

@pytest.mark.asyncio
async def test_create_order():
    # Arrange
    mock_service = AsyncMock()
    controller = OrdersController(mock_service)
    order = Order(item="Test Item", quantity=1)
    expected_order = Order(id=1, item="Test Item", quantity=1)
    mock_service.create.return_value = expected_order
    
    # Act
    result = await controller.create_order(order)
    
    # Assert
    assert result == expected_order
    mock_service.create.assert_called_once_with(order)

@pytest.mark.asyncio
async def test_get_all_orders():
    # Arrange
    mock_service = AsyncMock()
    controller = OrdersController(mock_service)
    expected_orders = [Order(id=1, item="Item1", quantity=1)]
    mock_service.get_all.return_value = expected_orders
    
    # Act
    result = await controller.get_all_orders()
    
    # Assert
    assert result == expected_orders
    mock_service.get_all.assert_called_once()

@pytest.mark.asyncio
async def test_get_order_by_id_found():
    # Arrange
    mock_service = AsyncMock()
    controller = OrdersController(mock_service)
    expected_order = Order(id=1, item="Test Item", quantity=1)
    mock_service.get_by_id.return_value = expected_order
    
    # Act
    result = await controller.get_order_by_id(1)
    
    # Assert
    assert result == expected_order
    mock_service.get_by_id.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_get_order_by_id_not_found():
    # Arrange
    mock_service = AsyncMock()
    controller = OrdersController(mock_service)
    mock_service.get_by_id.return_value = None
    
    # Act
    result = await controller.get_order_by_id(999)
    
    # Assert
    assert result is None
    mock_service.get_by_id.assert_called_once_with(999)

@pytest.mark.asyncio
async def test_update_order():
    # Arrange
    mock_service = AsyncMock()
    controller = OrdersController(mock_service)
    order = Order(item="Updated Item", quantity=2)
    expected_order = Order(id=1, item="Updated Item", quantity=2)
    mock_service.update.return_value = expected_order
    
    # Act
    result = await controller.update_order(1, order)
    
    # Assert
    assert result == expected_order
    mock_service.update.assert_called_once_with(1, order)

@pytest.mark.asyncio
async def test_delete_order():
    # Arrange
    mock_service = AsyncMock()
    controller = OrdersController(mock_service)
    mock_service.delete.return_value = True
    
    # Act
    result = await controller.delete_order(1)
    
    # Assert
    assert result is True
    mock_service.delete.assert_called_once_with(1)