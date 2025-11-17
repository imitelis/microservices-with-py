# src/infrastructure/inbound/api/routers/asyncapi_router.py
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import yaml
from src.core.asyncapi_spec import asyncapi_spec

def get_asyncapi_router():
    router = APIRouter()

    @router.get("/asyncapi.yaml", response_class=PlainTextResponse)
    async def asyncapi_yaml():
        return yaml.dump(asyncapi_spec, sort_keys=False)

    return router