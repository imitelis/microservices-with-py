# app/ports/order_repo.py

from typing import List, Optional
from abc import ABC, abstractmethod
from app.domain.models import Order

class OrderRepositoryPort(ABC):
    @abstractmethod
    async def save_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def get_all_orders(self) -> List[Order]:
        pass

    @abstractmethod
    async def get_order_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    async def update_order(self, order_id: int, order: Order) -> Optional[Order]:
        pass

    @abstractmethod
    async def delete_order(self, order_id: int) -> bool:
        pass
