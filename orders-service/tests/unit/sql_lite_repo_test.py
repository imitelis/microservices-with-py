import pytest
import asyncio
import aiosqlite
from app.adapters.outbound.sqlite_repo import SQLiteOrderRepository
from app.domain.models import Order

@pytest.mark.asyncio
async def test_init_creates_table(tmp_path):
    db_file = tmp_path / "test_orders.db"
    repo = SQLiteOrderRepository()
    repo.db_path = str(db_file)

    await repo.init()

    async with aiosqlite.connect(repo.db_path) as db:
        async with db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'") as cursor:
            row = await cursor.fetchone()
            assert row is not None
            assert row[0] == "orders"

