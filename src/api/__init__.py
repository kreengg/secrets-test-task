from fastapi import APIRouter

from .routers import router

api_router = APIRouter(
    prefix="/api",
)

api_router.include_router(router)
