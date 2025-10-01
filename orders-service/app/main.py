from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.adapters.outbound.kafka_producer import KafkaOrderProducer
from app.adapters.outbound.sqlite_repo import SQLiteOrderRepository
from app.application.order_service import OrderService
from app.adapters.inbound.api.routes import get_order_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    repo = SQLiteOrderRepository()
    producer = KafkaOrderProducer()

    await repo.init()
    await producer.start()

    app.state.repo = repo
    app.state.producer = producer

    # Create the use case and router here, after producer & repo are ready
    order_uc = OrderService(repo, producer)
    app.include_router(get_order_router(order_uc))

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
