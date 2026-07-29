from fastapi import FastAPI

from app.api.router import api_router
from app.core.logging import logger
from app.core.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
    )

    app.include_router(api_router)

    logger.info(f"{settings.APP_NAME} started successfully.")

    return app