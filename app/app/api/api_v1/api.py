from fastapi import APIRouter

from app.api.api_v1.endpoints import feeds, items, media, utils

api_router = APIRouter()
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(feeds.router, prefix="/feeds", tags=["feeds"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(media.router, prefix="/media", tags=["media"])
