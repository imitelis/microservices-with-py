# app/api/routes.py

from fastapi import APIRouter
from app.domain.models import Order
from app.use_cases.create_order import CreateOrderUseCase

def get_order_router(use_case: CreateOrderUseCase):
    router = APIRouter()

    @router.post("/orders")
    async def create_order(order: Order):
        result = await use_case.execute(order)
        return result

    return router
