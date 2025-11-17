# src/infrastructure/inbound/api/controllers/orders_controller.py
from src.domain.models.order import Order
from src.application.services.orders_service import OrdersService

class OrdersController:
    def __init__(self, service: OrdersService):
        self.service = service

    async def create_order(self, order: Order) -> Order:
        return await self.service.create(order)

    async def get_all_orders(self):
        return await self.service.get_all()

    async def get_order_by_id(self, order_id: int):
        order = await self.service.get_by_id(order_id)
        if not order:
            return None
        return order

    async def update_order(self, order_id: int, order: Order):
        return await self.service.update(order_id, order)

    async def delete_order(self, order_id: int):
        return await self.service.delete(order_id)
