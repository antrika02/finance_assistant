from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.core.logging import logger
from app.core.settings import get_settings
from app.database.session import engine
from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])

settings = get_settings()


@router.get(
    "/health",
    response_model=HealthResponse,
)
def health_check() -> HealthResponse:
    """
    Health check endpoint that verifies
    both the application and database.
    """

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return HealthResponse(
            status="healthy",
            database="connected",
            application=settings.APP_NAME,
            version=settings.APP_VERSION,
        )

    except Exception:  # noqa: BLE001
        logger.exception("Health check failed.")

        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "message": "Database connection failed.",
            },
        )
