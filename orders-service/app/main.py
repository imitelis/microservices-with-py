from fastapi import FastAPI
from app.adapters.kafka_producer import KafkaOrderProducer
from app.adapters.sqlite_repo import SQLiteOrderRepository
from app.logic.create_order import CreateOrderUseCase
from app.api.routes import get_order_router

app = FastAPI()

repo = SQLiteOrderRepository()
producer = None
use_case = None

@app.on_event("startup")
async def startup():
    global producer, use_case
    await repo.init()
    producer = KafkaOrderProducer()
    await producer.start()
    use_case = CreateOrderUseCase(repo, producer)
    app.include_router(get_order_router(use_case))

@app.on_event("shutdown")
async def shutdown():
    await producer.stop()
