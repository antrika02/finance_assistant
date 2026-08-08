from fastapi import APIRouter

from app.core.settings import get_settings

router = APIRouter(tags=["Root"])

settings = get_settings()


@router.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "environment": settings.APP_ENV,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "message": "Welcome to the FinPilot AI API 🚀",
    }
