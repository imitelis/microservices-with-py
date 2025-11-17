# app/domain/order.py

from pydantic import BaseModel

class Order(BaseModel):
    id: int | None = None
    item: str
    quantity: int
