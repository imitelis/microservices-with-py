import pytest
from src.domain.models.order import Order
from src.application.services.orders_service import OrderService

class DummyRepo:
    async def save_order(self, order):
        order.id = 1
        return order

class DummyProducer:
    async def send_order(self, order):
        pass

@pytest.mark.asyncio
async def test_create_order():
    use_case = OrderService(DummyRepo(), DummyProducer())
    order = Order(item="Keyboard", quantity=2)
    saved = await use_case.create(order)
    assert saved.id == 1
    assert saved.item == "Keyboard"
