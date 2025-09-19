from app.domain.models import Order
from app.ports.order_repo import OrderRepositoryPort
from app.ports.order_publisher import OrderPublisherPort

class CreateOrderUseCase:
    def __init__(self, repo: OrderRepositoryPort, producer: OrderPublisherPort):
        self.repo = repo
        self.producer = producer

    async def execute(self, order: Order) -> Order:
        saved = await self.repo.save_order(order)
        await self.producer.send_order(saved)
        return saved
