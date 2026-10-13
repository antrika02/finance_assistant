from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import computed_field, model_validator
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

    @model_validator(mode="after")
    def validate_production_configuration(self):
        """
        Validate security-sensitive configuration when running
        in production.
        """

        if self.APP_ENV.lower() != "production":
            return self

        if self.DEBUG:
            raise ValueError("DEBUG must be False when APP_ENV=production.")

        if len(self.SECRET_KEY) < 32:
            raise ValueError(
                "SECRET_KEY must be at least 32 characters long "
                "when APP_ENV=production."
            )

        if self.BACKEND_CORS_ORIGINS.strip() == "*":
            raise ValueError(
                "BACKEND_CORS_ORIGINS must explicitly define trusted "
                "origins when APP_ENV=production."
            )

        if not self.DATABASE_URL_OVERRIDE:
            raise ValueError(
                "DATABASE_URL_OVERRIDE must be configured when APP_ENV=production."
            )

        return self

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """
        Return the database connection string.

        Uses DATABASE_URL_OVERRIDE when provided (for example, Neon or Render).
        Otherwise, constructs a URL from the individual database settings.

        URL-encodes the username and password to safely handle special
        characters such as @, :, /, #, and %.
        """

        if self.DATABASE_URL_OVERRIDE:
            url = self.DATABASE_URL_OVERRIDE

            if url.startswith("postgres://"):
                url = url.replace(
                    "postgres://",
                    "postgresql+psycopg://",
                    1,
                )
            elif url.startswith("postgresql://"):
                url = url.replace(
                    "postgresql://",
                    "postgresql+psycopg://",
                    1,
                )

            return url

        user = quote_plus(self.DATABASE_USER)
        password = quote_plus(self.DATABASE_PASSWORD)

        return (
            f"postgresql+psycopg://"
            f"{user}:{password}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )


@lru_cache
def get_settings() -> Settings:
    """
    Return the cached application settings.
    """
    return Settings()