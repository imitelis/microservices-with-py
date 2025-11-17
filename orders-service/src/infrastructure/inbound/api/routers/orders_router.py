# src/infrastructure/inbound/api/routers/orders_router.py

from typing import List
from fastapi import APIRouter, HTTPException
from src.domain.models.order import Order
from src.application.controllers.orders_controller import OrdersController
from src.application.services.orders_service import OrdersService

def get_orders_router(order_service: OrdersService):
    controller = OrdersController(order_service)
    router = APIRouter()

    @router.post("/orders", response_model=Order)
    async def create_order(order: Order) -> Order:
        return await controller.create_order(order)

    @router.get("/orders", response_model=List[Order])
    async def get_all_orders() -> List[Order]:
        return await controller.get_all_orders()

    @router.get("/orders/{order_id}", response_model=Order)
    async def get_order_by_id(order_id: int) -> Order:
        order = await controller.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    @router.patch("/orders/{order_id}", response_model=Order)
    async def update_order(order_id: int, order: Order) -> Order:
        updated = await controller.update_order(order_id, order)
        if not updated:
            raise HTTPException(status_code=404, detail="Order not found")
        return updated

    @router.delete("/orders/{order_id}", status_code=204)
    async def delete_order(order_id: int):
        deleted = await controller.delete_order(order_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Order not found")
        return

    return router