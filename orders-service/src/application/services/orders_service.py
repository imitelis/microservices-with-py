from typing import List, Optional
from src.domain.models.order import Order
from src.domain.ports.order_repo import OrderRepositoryPort
from src.domain.ports.order_publisher import OrderPublisherPort

class OrdersService:
    def __init__(self, repo: OrderRepositoryPort, producer: OrderPublisherPort):
        self.repo = repo
        self.producer = producer

    async def create(self, order: Order) -> Order:
        saved = await self.repo.save_order(order)
        await self.producer.send_order(saved)
        return saved

    async def get_all(self) -> List[Order]:
        return await self.repo.get_all_orders()

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        return await self.repo.get_order_by_id(order_id)

    async def update(self, order_id: int, order: Order) -> Optional[Order]:
        return await self.repo.update_order(order_id, order)

    async def delete(self, order_id: int) -> bool:
        return await self.repo.delete_order(order_id)

