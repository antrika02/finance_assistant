from fastapi import FastAPI

from app.api.router import api_router
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import logger
from app.core.settings import get_settings
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    # Register global exception handlers
    register_exception_handlers(app)

    # Register all API routes
    app.include_router(api_router)

    logger.info(f"{settings.APP_NAME} started successfully.")

    return app