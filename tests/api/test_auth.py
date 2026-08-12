from datetime import UTC, datetime, timedelta

from jose import jwt

from app.core.settings import get_settings
from tests.auth import auth_headers
from tests.factories import user_payload


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
    payload = user_payload()

    client.post(
        "/auth/register",
        json=payload,
    )

    response = client.post(
        "/auth/login",
        data={
            "username": payload["email"],
            "password": payload["password"],
        },
    )

    assert response.status_code == 200

    assert "access_token" in response.json()


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
        "sub": "test@example.com",
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
