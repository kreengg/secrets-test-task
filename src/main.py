from fastapi import FastAPI

from src.api import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Secrets",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    app.include_router(api_router)
    return app
