# src/ports/order_publisher.py
from abc import ABC, abstractmethod
from src.domain.models.order import Order

class OrderPublisherPort(ABC):
    @abstractmethod
    async def send_order(self, order: Order):
        pass
