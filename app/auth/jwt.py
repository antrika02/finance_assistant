from datetime import UTC, datetime, timedelta

from jose import jwt

from app.core.settings import get_settings

settings = get_settings()


def create_access_token(subject: str) -> str:
    """
    Create a JWT access token.

    The subject should contain the immutable user identifier.
    """
    now = datetime.now(UTC)
    expire = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    payload = {
        "sub": subject,
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT.
    """
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )