from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Secrets",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    return app
