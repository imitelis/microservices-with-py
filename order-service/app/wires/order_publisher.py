# app/ports/order_publisher.py
from abc import ABC, abstractmethod
from app.domain.models import Order

class OrderPublisherPort(ABC):
    @abstractmethod
    async def send_order(self, order: Order):
        pass
