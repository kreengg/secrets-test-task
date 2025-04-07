from fastapi import FastAPI, Request, Response

from src.api import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Secrets",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    @app.middleware("http")
    async def add_no_cache_headers(request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    app.include_router(api_router)
    return app
