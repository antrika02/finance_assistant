import pytest
from pydantic import ValidationError

from app.core.settings import Settings

TEST_DATABASE_URL = "postgresql://user:password@db.example.com/finpilot"


def test_development_allows_wildcard_cors():
    settings = Settings(
        SECRET_KEY="test-secret",
        GEMINI_API_KEY="test-gemini-key",
        APP_ENV="development",
        BACKEND_CORS_ORIGINS="*",
    )

    assert settings.BACKEND_CORS_ORIGINS == "*"


def test_production_allows_explicit_cors_origins():
    settings = Settings(
        SECRET_KEY="a" * 32,
        GEMINI_API_KEY="test-gemini-key",
        APP_ENV="production",
        DEBUG=False,
        BACKEND_CORS_ORIGINS="https://finpilot.example.com",
        DATABASE_URL_OVERRIDE=TEST_DATABASE_URL,
    )

    assert settings.BACKEND_CORS_ORIGINS == "https://finpilot.example.com"


def test_production_rejects_debug_mode():
    with pytest.raises(
        ValidationError,
        match="DEBUG must be False",
    ):
        Settings(
            SECRET_KEY="a" * 32,
            GEMINI_API_KEY="test-gemini-key",
            APP_ENV="production",
            DEBUG=True,
            BACKEND_CORS_ORIGINS="https://finpilot.example.com",
            DATABASE_URL_OVERRIDE=TEST_DATABASE_URL,
        )


def test_production_rejects_weak_secret_key():
    with pytest.raises(
        ValidationError,
        match="SECRET_KEY must be at least 32 characters",
    ):
        Settings(
            SECRET_KEY="short-secret",
            GEMINI_API_KEY="test-gemini-key",
            APP_ENV="production",
            DEBUG=False,
            BACKEND_CORS_ORIGINS="https://finpilot.example.com",
            DATABASE_URL_OVERRIDE=TEST_DATABASE_URL,
        )


def test_production_rejects_wildcard_cors():
    with pytest.raises(
        ValidationError,
        match="BACKEND_CORS_ORIGINS",
    ):
        Settings(
            SECRET_KEY="a" * 32,
            GEMINI_API_KEY="test-gemini-key",
            APP_ENV="production",
            DEBUG=False,
            BACKEND_CORS_ORIGINS="*",
            DATABASE_URL_OVERRIDE=TEST_DATABASE_URL,
        )


def test_production_rejects_missing_database_url():
    with pytest.raises(
        ValidationError,
        match="DATABASE_URL_OVERRIDE",
    ):
        Settings(
            SECRET_KEY="a" * 32,
            GEMINI_API_KEY="test-gemini-key",
            APP_ENV="production",
            DEBUG=False,
            BACKEND_CORS_ORIGINS="https://finpilot.example.com",
            DATABASE_URL_OVERRIDE=None,
        )


def test_database_url_converts_postgresql_scheme():
    settings = Settings(
        SECRET_KEY="test-secret",
        GEMINI_API_KEY="test-gemini-key",
        APP_ENV="development",
        DATABASE_URL_OVERRIDE=TEST_DATABASE_URL,
    )

    assert (
        settings.DATABASE_URL
        == "postgresql+psycopg://user:password@db.example.com/finpilot"
    )


def test_database_url_converts_legacy_postgres_scheme():
    settings = Settings(
        SECRET_KEY="test-secret",
        GEMINI_API_KEY="test-gemini-key",
        APP_ENV="development",
        DATABASE_URL_OVERRIDE=("postgres://user:password@db.example.com/finpilot"),
    )

    assert (
        settings.DATABASE_URL
        == "postgresql+psycopg://user:password@db.example.com/finpilot"
    )
