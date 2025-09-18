# app/ports/order_repo.py

from abc import ABC, abstractmethod
from app.domain.models import Order

class OrderRepositoryPort(ABC):
    @abstractmethod
    async def save_order(self, order: Order) -> Order:
        pass
