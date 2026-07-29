from fastapi import APIRouter

from app.core.settings import get_settings

router = APIRouter(tags=["Health"])

settings = get_settings()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
    }