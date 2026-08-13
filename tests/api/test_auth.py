from datetime import UTC, datetime, timedelta

from jose import jwt
from sqlalchemy import select

from app.core.settings import get_settings
from app.models.user import User
from tests.auth import auth_headers
from tests.database import TestingSessionLocal
from tests.factories import user_payload


def deactivate_user(email: str) -> None:
    """
    Deactivate a user directly in the test database.
    """
    db = TestingSessionLocal()

    try:
        user = db.scalar(
            select(User).where(User.email == email),
        )

        assert user is not None

        user.is_active = False
        db.commit()
    finally:
        db.close()


def test_register_user(client):
    payload = user_payload()

    response = client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["email"] == payload["email"]
    assert body["full_name"] == payload["full_name"]


def test_duplicate_email(client):
    payload = user_payload()

    client.post(
        "/auth/register",
        json=payload,
    )

    response = client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 409


def test_login_success(client):
    settings = get_settings()
    payload = user_payload()

    register_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert register_response.status_code == 201

    user_id = register_response.json()["id"]

    response = client.post(
        "/auth/login",
        data={
            "username": payload["email"],
            "password": payload["password"],
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    decoded = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    assert decoded["sub"] == str(user_id)
    assert "iat" in decoded
    assert "exp" in decoded
    assert decoded["exp"] > decoded["iat"]


def test_login_invalid_password(client):
    payload = user_payload()

    client.post(
        "/auth/register",
        json=payload,
    )

    response = client.post(
        "/auth/login",
        data={
            "username": payload["email"],
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_login_inactive_user(client):
    payload = user_payload()

    client.post(
        "/auth/register",
        json=payload,
    )

    deactivate_user(payload["email"])

    response = client.post(
        "/auth/login",
        data={
            "username": payload["email"],
            "password": payload["password"],
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_current_user(client):
    headers = auth_headers(client)

    response = client.get(
        "/auth/me",
        headers=headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert "email" in body
    assert "id" in body


def test_current_user_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_current_user_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token."


def test_current_user_with_expired_token(client):
    settings = get_settings()

    expired_payload = {
        "sub": "1",
        "exp": datetime.now(UTC) - timedelta(minutes=1),
    }

    token = jwt.encode(
        expired_payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token."


def test_current_user_with_token_without_subject(client):
    settings = get_settings()

    payload = {
        "exp": datetime.now(UTC) + timedelta(minutes=30),
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token."


def test_current_user_with_invalid_subject(client):
    settings = get_settings()

    payload = {
        "sub": "not-a-user-id",
        "exp": datetime.now(UTC) + timedelta(minutes=30),
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token."


def test_inactive_user_cannot_use_existing_token(client):
    payload = user_payload()

    client.post(
        "/auth/register",
        json=payload,
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": payload["email"],
            "password": payload["password"],
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    deactivate_user(payload["email"])

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or inactive account."