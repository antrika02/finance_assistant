import pytest
from pydantic import ValidationError

from app.core.settings import Settings


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
    )

    assert (
        settings.BACKEND_CORS_ORIGINS
        == "https://finpilot.example.com"
    )


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
        )