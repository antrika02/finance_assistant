from tests.factories import user_payload


def register_user(client):
    payload = user_payload()

    response = client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 201

    return payload


def login_user(client, payload):
    response = client.post(
        "/auth/login",
        data={
            "username": payload["email"],
            "password": payload["password"],
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def auth_headers(client):
    payload = register_user(client)

    token = login_user(client, payload)

    return {
        "Authorization": f"Bearer {token}"
    }