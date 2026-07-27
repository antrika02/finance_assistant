from fastapi import FastAPI

from app.core.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "environment": settings.APP_ENV,
    }