from fastapi import FastAPI
from app.adapters.kafka_producer import KafkaOrderProducer
from app.adapters.sqlite_repo import SQLiteOrderRepository
from app.application.create_order import CreateOrderUseCase
from app.api.routes import get_order_router

def create_app() -> FastAPI:
    app = FastAPI()
    repo = SQLiteOrderRepository()
    producer = KafkaOrderProducer()
    use_case = CreateOrderUseCase(repo, producer)

    app.include_router(get_order_router(use_case))

    @app.on_event("startup")
    async def startup():
        await repo.init()
        await producer.start()

    @app.on_event("shutdown")
    async def shutdown():
        await producer.stop()

    return app

app = create_app()