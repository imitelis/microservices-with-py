# src/infrastructure/outbound/db/sqlite_repo.py

import aiosqlite
from typing import List, Optional
from src.domain.models.order import Order
from src.domain.ports.order_repo import OrderRepositoryPort
from src.core.config import SQLITE_DB_FILE

class SQLiteOrderRepository(OrderRepositoryPort):
    def __init__(self):
        self.db_path = SQLITE_DB_FILE

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item TEXT,
                    quantity INTEGER
                )
            """)
            await db.commit()

    async def save_order(self, order: Order) -> Order:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO orders (item, quantity) VALUES (?, ?)",
                (order.item, order.quantity)
            )
            await db.commit()
            order.id = cursor.lastrowid
        return order
    
    async def get_all_orders(self) -> List[Order]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT id, item, quantity FROM orders")
            rows = await cursor.fetchall()
            return [Order(id=row[0], item=row[1], quantity=row[2]) for row in rows]
        
    async def get_order_by_id(self, order_id: int) -> Optional[Order]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT id, item, quantity FROM orders WHERE id = ?", (order_id,))
            row = await cursor.fetchone()
            if row:
                return Order(id=row[0], item=row[1], quantity=row[2])
            return None

    async def update_order(self, order_id: int, order: Order) -> Optional[Order]:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE orders SET item = ?, quantity = ? WHERE id = ?",
                (order.item, order.quantity, order_id)
            )
            await db.commit()
            return await self.get_order_by_id(order_id)

    async def delete_order(self, order_id: int) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("DELETE FROM orders WHERE id = ?", (order_id,))
            await db.commit()
            return cursor.rowcount > 0
