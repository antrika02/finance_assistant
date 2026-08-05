from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    # ------------------------------------------------------------------
    # Application Settings
    # ------------------------------------------------------------------
    APP_NAME: str = "FinPilot AI"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ------------------------------------------------------------------
    # Security
    # ------------------------------------------------------------------
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    # Used in production (Render + Neon)
    DATABASE_URL: str | None = None

    # Used for local development
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "personal_finance"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"

    # ------------------------------------------------------------------
    # Gemini AI
    # ------------------------------------------------------------------
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # ------------------------------------------------------------------
    # Pydantic Settings Configuration
    # ------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Computed Database URL
    # ------------------------------------------------------------------
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        """
        Returns the SQLAlchemy database URL.

        Priority:
        1. DATABASE_URL (Render / Neon)
        2. Local database credentials
        """

        if self.DATABASE_URL:
            # Neon provides:
            # postgresql://...
            # SQLAlchemy expects:
            # postgresql+psycopg://...
            return self.DATABASE_URL.replace(
                "postgresql://",
                "postgresql+psycopg://",
                1,
            )

        return (
            f"postgresql+psycopg://"
            f"{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    """
    return Settings()