# src/infrastructure/inbound/api/routers/asyncapi_router.py
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from src.core.asyncapi_utils import generate_asyncapi_spec, asyncapi_yaml_from_spec
from src.domain.models.order import Order
from src.core.config import KAFKA_BOOTSTRAP_SERVERS, TOPIC_ORDERS

def get_asyncapi_router() -> APIRouter:
    router = APIRouter()

    @router.get("/asyncapi.yaml", response_class=PlainTextResponse)
    async def asyncapi_yaml():
        spec = generate_asyncapi_spec(
            topic=TOPIC_ORDERS,
            model=Order,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
        )
        return asyncapi_yaml_from_spec(spec)

    return router
