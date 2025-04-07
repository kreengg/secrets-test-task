from fastapi import APIRouter

from .secret import router as secrets_router

router = APIRouter()

router.include_router(secrets_router)
