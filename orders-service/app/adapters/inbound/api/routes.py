# app/api/routes.py

from typing import List
from fastapi import APIRouter, HTTPException
from app.domain.models import Order
from app.application.order_service import OrderService

def get_order_router(
    order_service: OrderService
):
    router = APIRouter()

    @router.post("/orders", response_model=Order)
    async def create_order(order: Order) -> Order:
        result = await order_service.create(order)
        return result

    @router.get("/orders", response_model=List[Order])
    async def get_all_orders() -> List[Order]:
        return await order_service.get_all()
    
    @router.get("/orders/{order_id}", response_model=Order)
    async def get_order_by_id(order_id: int) -> Order:
        order = await order_service.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    @router.patch("/orders/{order_id}", response_model=Order)
    async def update_order(order_id: int, order: Order) -> Order:
        updated = await order_service.update(order_id, order)
        if not updated:
            raise HTTPException(status_code=404, detail="Order not found")
        return updated

    @router.delete("/orders/{order_id}", status_code=204)
    async def delete_order(order_id: int):
        deleted = await order_service.delete(order_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Order not found")
        return

    return router

