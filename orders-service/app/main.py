from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.adapters.kafka_producer import KafkaOrderProducer
from app.adapters.sqlite_repo import SQLiteOrderRepository
from app.application.create_order import CreateOrderUseCase
from app.api.routes import get_order_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    repo = SQLiteOrderRepository()
    producer = KafkaOrderProducer()

    await repo.init()
    await producer.start()

    app.state.repo = repo
    app.state.producer = producer

    # Create the use case and router here, after producer & repo are ready
    use_case = CreateOrderUseCase(repo, producer)
    app.include_router(get_order_router(use_case))

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
