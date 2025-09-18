# app/adapters/sqlite_repo.py

import aiosqlite
from app.domain.models import Order
from app.ports.order_repo import OrderRepositoryPort
from app.config import SQLITE_DB_FILE

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
