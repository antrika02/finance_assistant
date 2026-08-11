from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    # --------------------------------------------------
    # Application
    # --------------------------------------------------
    APP_NAME: str = "FinPilot AI"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # --------------------------------------------------
    # Security
    # --------------------------------------------------
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --------------------------------------------------
    # Database
    # --------------------------------------------------

    # Optional full connection string (used in production)
    DATABASE_URL_OVERRIDE: str | None = None

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "personal_finance"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"

    # --------------------------------------------------
    # Gemini
    # --------------------------------------------------
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # --------------------------------------------------
    # CORS
    # --------------------------------------------------
    BACKEND_CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """
        Returns the database connection string.

        Uses DATABASE_URL_OVERRIDE when provided (Render/Neon),
        otherwise constructs a local PostgreSQL URL.
        """
        if self.DATABASE_URL_OVERRIDE:
            url = self.DATABASE_URL_OVERRIDE

            if url.startswith("postgresql://"):
                url = url.replace(
                    "postgresql://",
                    "postgresql+psycopg://",
                    1,
                )

            elif url.startswith("postgres://"):
                url = url.replace(
                    "postgres://",
                    "postgresql+psycopg://",
                    1,
                )

            return url

        return (
            f"postgresql+psycopg://"
            f"{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
