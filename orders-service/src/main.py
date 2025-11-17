from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.infrastructure.outbound.messaging.kafka_producer import KafkaOrderProducer
from src.infrastructure.outbound.db.sqlite_repo import SQLiteOrderRepository 
from src.application.services.orders_service import OrdersService
from src.infrastructure.inbound.api.routers.orders_router import get_orders_router
from src.infrastructure.inbound.api.routers.asyncapi_router import get_asyncapi_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    repo = SQLiteOrderRepository()
    producer = KafkaOrderProducer()

    await repo.init()
    await producer.start(retries=10, delay=2)

    app.state.repo = repo
    app.state.producer = producer

    # Create the use case and router here, after producer & repo are ready
    order_uc = OrdersService(repo, producer)
    app.include_router(get_orders_router(order_uc))
    app.include_router(get_asyncapi_router())

    yield

    await producer.stop()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    
    # Define a simple root route so "/" returns 200
    @app.get("/")
    async def root():
        return {"status": "ok"}

    return app

app = create_app()
