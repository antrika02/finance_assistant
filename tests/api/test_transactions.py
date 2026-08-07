from tests.auth import (
    create_category,
    create_transaction,
)

from tests.fixtures.users import create_authenticated_user

from tests.fixtures.categories import create_user_category

from tests.fixtures.transactions import create_user_transaction


def test_create_transaction(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    response = client.post(
        "/transactions/",
        json={
            "amount": 250,
            "type": "expense",
            "description": "Lunch",
            "transaction_date": "2026-08-01",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["amount"] == "250.00"
    assert body["type"] == "expense"
    assert body["description"] == "Lunch"
    assert body["category_id"] == category["id"]


def test_get_transactions(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    create_transaction(
        client,
        authenticated_headers,
        category["id"],
    )

    response = client.get(
        "/transactions/",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["total"] == 1
    assert len(body["items"]) == 1


def test_get_transaction_by_id(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    transaction = create_transaction(
        client,
        authenticated_headers,
        category["id"],
    )

    response = client.get(
        f"/transactions/{transaction['id']}",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    assert response.json()["id"] == transaction["id"]


def test_update_transaction(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    transaction = create_transaction(
        client,
        authenticated_headers,
        category["id"],
    )

    response = client.put(
        f"/transactions/{transaction['id']}",
        json={
            "amount": 500,
            "description": "Dinner",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["amount"] == "500.00"
    assert body["description"] == "Dinner"


def test_delete_transaction(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    transaction = create_transaction(
        client,
        authenticated_headers,
        category["id"],
    )

    response = client.delete(
        f"/transactions/{transaction['id']}",
        headers=authenticated_headers,
    )

    assert response.status_code == 204

    response = client.get(
        f"/transactions/{transaction['id']}",
        headers=authenticated_headers,
    )

    assert response.status_code == 404


def test_transaction_not_found(
    client,
    authenticated_headers,
):
    response = client.get(
        "/transactions/99999",
        headers=authenticated_headers,
    )

    assert response.status_code == 404

def test_invalid_category(
    client,
    authenticated_headers,
):
    response = client.post(
        "/transactions/",
        json={
            "amount": 100,
            "type": "expense",
            "description": "Lunch",
            "transaction_date": "2026-08-01",
            "category_id": 99999,
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 400

def test_get_transactions_without_token(
    client,
):
    response = client.get("/transactions/")

    assert response.status_code == 401


def test_cannot_access_other_users_transaction(client):

    user1 = create_authenticated_user(client)

    user2 = create_authenticated_user(

        client,

        email="another@example.com",

    )

    category = create_user_category(

        client,

        user1,

    )

    transaction = create_user_transaction(

        client,

        user1,

        category["id"],

    )

    response = client.get(

        f"/transactions/{transaction['id']}",

        headers=user2.headers,

    )

    assert response.status_code == 403