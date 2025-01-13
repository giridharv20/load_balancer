from fastapi import APIRouter

from src.container.container import container as ctx
from src.entities.key_value import KeyValue

router = APIRouter(prefix="/urls")

@router.post("/register_url")
async def register_url(item: KeyValue):
    response = ctx.get("UrlService").register_service_url(item.key, item.value)
    return response

@router.post("/deregister_url")
async def deregister_url(item: KeyValue):
    response = ctx.get("UrlService").deregister_service_url(item.key, item.value)
    return response

@router.post("/unhealthy_url")
async def unhealthy_url(item: KeyValue):
    response = ctx.get("UrlService").unhealthy_service_url(item.key, item.value)
    return response

@router.get("/ping")
async def ping():
    return ctx.get("UrlService").ping()
