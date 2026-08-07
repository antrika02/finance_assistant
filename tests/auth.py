from tests.factories import (
    category_payload,
    transaction_payload,
    user_payload,
)


def register_user(

    client,

    full_name="John Doe",

    email=None,

    password="Password123!",

):

    payload = user_payload(

        full_name=full_name,

        email=email,

        password=password,

    )

    response = client.post(

        "/auth/register",

        json=payload,

    )

    assert response.status_code == 201

    return payload


def login_user(client, payload):
    """
    Login an existing user.
    """
    response = client.post(
        "/auth/login",
        data={
            "username": payload["email"],
            "password": payload["password"],
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def auth_headers(
    client,
    full_name="John Doe",
    email=None,
    password="Password123!",
):
    payload = register_user(
        client,
        full_name=full_name,
        email=email,
        password=password,
    )

    token = login_user(client, payload)

    return {
        "Authorization": f"Bearer {token}"
    }


def create_category(client, headers, **kwargs):
    """
    Creates a category and returns its JSON.
    """
    payload = category_payload(**kwargs)

    response = client.post(
        "/categories/",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 201

    return response.json()


def create_transaction(
    client,
    headers,
    category_id,
    **kwargs,
):
    """
    Creates a transaction and returns its JSON.
    """
    payload = transaction_payload(
        category_id=category_id,
        **kwargs,
    )

    response = client.post(
        "/transactions/",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 201

    return response.json()