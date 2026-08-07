from tests.auth import (
    create_category,
    create_transaction,
)
from decimal import Decimal
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

def test_transaction_pagination(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    for i in range(25):
        create_transaction(
            client,
            authenticated_headers,
            category["id"],
        )

    response = client.get(
        "/transactions?page=1&size=10",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["items"]) == 10
    assert body["page"] == 1
    assert body["size"] == 10
    assert body["total"] == 25
    assert body["pages"] == 3


def test_filter_transactions_by_type(
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

    client.post(
        "/transactions/",
        json={
            "amount": 1000,
            "type": "income",
            "description": "Salary",
            "transaction_date": "2026-08-01",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    response = client.get(
        "/transactions?type=income",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["items"]) == 1
    assert body["items"][0]["type"] == "income"

def test_search_transactions(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    client.post(
        "/transactions/",
        json={
            "amount": 200,
            "type": "expense",
            "description": "Pizza",
            "transaction_date": "2026-08-01",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    client.post(
        "/transactions/",
        json={
            "amount": 300,
            "type": "expense",
            "description": "Movie",
            "transaction_date": "2026-08-01",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    response = client.get(
        "/transactions?search=Pizza",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["items"]) == 1
    assert body["items"][0]["description"] == "Pizza"


def test_transaction_summary(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    client.post(
        "/transactions/",
        json={
            "amount": 1000,
            "type": "income",
            "description": "Salary",
            "transaction_date": "2026-08-01",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    client.post(
        "/transactions/",
        json={
            "amount": 400,
            "type": "expense",
            "description": "Rent",
            "transaction_date": "2026-08-01",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    response = client.get(
        "/transactions/summary",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    from decimal import Decimal

    assert Decimal(body["total_income"]) == Decimal("1000")
    assert Decimal(body["total_expense"]) == Decimal("400")
    assert Decimal(body["balance"]) == Decimal("600")

def test_transaction_pagination(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    for i in range(25):
        client.post(
            "/transactions/",
            json={
                "amount": i + 1,
                "type": "expense",
                "description": f"Expense {i}",
                "transaction_date": "2026-08-01",
                "category_id": category["id"],
            },
            headers=authenticated_headers,
        )

    response = client.get(
        "/transactions?page=1&size=10",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["page"] == 1
    assert body["size"] == 10
    assert body["total"] == 25
    assert body["pages"] == 3
    assert len(body["items"]) == 10


def test_filter_transactions_by_type(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    # Income transaction
    client.post(
        "/transactions/",
        json={
            "amount": 1000,
            "type": "income",
            "description": "Salary",
            "transaction_date": "2026-08-01",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    # Expense transaction
    client.post(
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

    response = client.get(
        "/transactions?type=income",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["total"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["type"] == "income"
    assert body["items"][0]["description"] == "Salary"

def test_filter_transactions_by_category(
    client,
    authenticated_headers,
):
    food = create_category(
        client,
        authenticated_headers,
    )

    travel = client.post(
        "/categories/",
        json={
            "name": "Travel",
            "type": "expense",
            "icon": "✈️",
            "color": "#0000FF",
        },
        headers=authenticated_headers,
    ).json()

    client.post(
        "/transactions/",
        json={
            "amount": 250,
            "type": "expense",
            "description": "Lunch",
            "transaction_date": "2026-08-01",
            "category_id": food["id"],
        },
        headers=authenticated_headers,
    )

    client.post(
        "/transactions/",
        json={
            "amount": 1000,
            "type": "expense",
            "description": "Flight",
            "transaction_date": "2026-08-01",
            "category_id": travel["id"],
        },
        headers=authenticated_headers,
    )

    response = client.get(
        f"/transactions?category_id={food['id']}",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["total"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["description"] == "Lunch"


def test_filter_transactions_by_date_range(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    # January transaction
    client.post(
        "/transactions/",
        json={
            "amount": 100,
            "type": "expense",
            "description": "January",
            "transaction_date": "2026-01-15",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    # February transaction
    client.post(
        "/transactions/",
        json={
            "amount": 200,
            "type": "expense",
            "description": "February",
            "transaction_date": "2026-02-15",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    response = client.get(
        "/transactions?start_date=2026-02-01&end_date=2026-02-28",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["total"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["description"] == "February"

def test_search_transactions(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    client.post(
        "/transactions/",
        json={
            "amount": 300,
            "type": "expense",
            "description": "Pizza Hut",
            "transaction_date": "2026-08-01",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    client.post(
        "/transactions/",
        json={
            "amount": 500,
            "type": "expense",
            "description": "Movie Night",
            "transaction_date": "2026-08-01",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    response = client.get(
        "/transactions?search=pizza",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["total"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["description"] == "Pizza Hut"


def test_sort_transactions_by_amount(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    for amount in [500, 100, 300]:
        client.post(
            "/transactions/",
            json={
                "amount": amount,
   
             "type": "expense",
                "description": f"{amount}",
                "transaction_date": "2026-08-01",
                "category_id": category["id"],
            },
            headers=authenticated_headers,
        )

    response = client.get(
        "/transactions?sort=amount",
        headers=authenticated_headers,
    )

    body = response.json()

    amounts = [float(item["amount"]) for item in body["items"]]

    assert amounts == [100, 300, 500]


def test_sort_transactions_by_date(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    dates = [
        "2026-03-01",
        "2026-01-01",
        "2026-02-01",
    ]

    for d in dates:
        client.post(
            "/transactions/",
            json={
                "amount": 100,
                "type": "expense",
                "description": d,
                "transaction_date": d,
                "category_id": category["id"],
            },
            headers=authenticated_headers,
        )

    response = client.get(
        "/transactions?sort=transaction_date",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    returned_dates = [
        item["transaction_date"]
        for item in body["items"]
    ]

    assert returned_dates == [
        "2026-01-01",
        "2026-02-01",
        "2026-03-01",
    ]