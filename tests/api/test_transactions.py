from tests.auth import (
    create_category,
    create_transaction,
)


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