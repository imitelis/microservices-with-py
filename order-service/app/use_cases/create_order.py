# app/use_cases/create_order.py

from app.domain.models import Order
from app.ports.order_repo import OrderRepositoryPort
from app.adapters.kafka_producer import KafkaOrderProducer

class CreateOrderUseCase:
    def __init__(self, repo: OrderRepositoryPort, producer: KafkaOrderProducer):
        self.repo = repo
        self.producer = producer

    async def execute(self, order: Order) -> Order:
        saved = await self.repo.save_order(order)
        await self.producer.send_order(saved)
        return saved
