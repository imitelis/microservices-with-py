import pytest
from app.domain.models import Order
from app.application.create_order import CreateOrderUseCase

class DummyRepo:
    async def save_order(self, order):
        order.id = 1
        return order

class DummyProducer:
    async def send_order(self, order):
        pass

@pytest.mark.asyncio
async def test_create_order():
    use_case = CreateOrderUseCase(DummyRepo(), DummyProducer())
    order = Order(item="Keyboard", quantity=2)
    saved = await use_case.execute(order)
    assert saved.id == 1
    assert saved.item == "Keyboard"
