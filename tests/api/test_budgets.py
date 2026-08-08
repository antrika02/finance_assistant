from decimal import Decimal

from tests.auth import create_category
from tests.fixtures.categories import create_user_category
from tests.fixtures.users import create_authenticated_user


def create_budget(
    client,
    headers,
    category_id,
    amount=5000,
    month=8,
    year=2026,
):
    response = client.post(
        "/budgets",
        json={
            "amount": amount,
            "month": month,
            "year": year,
            "category_id": category_id,
        },
        headers=headers,
    )

    assert response.status_code == 201

    return response.json()


def test_create_budget(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    response = client.post(
        "/budgets",
        json={
            "amount": 5000,
            "month": 8,
            "year": 2026,
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert Decimal(body["amount"]) == Decimal("5000.00")
    assert body["month"] == 8
    assert body["year"] == 2026
    assert body["category_id"] == category["id"]


def test_get_budgets(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    create_budget(
        client,
        authenticated_headers,
        category["id"],
    )

    response = client.get(
        "/budgets",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert Decimal(body[0]["amount"]) == Decimal("5000.00")


def test_update_budget(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    budget = create_budget(
        client,
        authenticated_headers,
        category["id"],
    )

    response = client.put(
        f"/budgets/{budget['id']}",
        json={
            "amount": 7500,
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert Decimal(body["amount"]) == Decimal("7500.00")


def test_delete_budget(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    budget = create_budget(
        client,
        authenticated_headers,
        category["id"],
    )

    response = client.delete(
        f"/budgets/{budget['id']}",
        headers=authenticated_headers,
    )

    assert response.status_code == 204

    response = client.get(
        "/budgets",
        headers=authenticated_headers,
    )

    assert response.status_code == 200
    assert response.json() == []


def test_budget_not_found(
    client,
    authenticated_headers,
):
    response = client.put(
        "/budgets/99999",
        json={
            "amount": 1000,
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 404


def test_get_budgets_without_token(
    client,
):
    response = client.get("/budgets")

    assert response.status_code == 401


def test_duplicate_budget(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    create_budget(
        client,
        authenticated_headers,
        category["id"],
        amount=5000,
        month=8,
        year=2026,
    )

    response = client.post(
        "/budgets",
        json={
            "amount": 7000,
            "month": 8,
            "year": 2026,
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 409


def test_invalid_category(
    client,
    authenticated_headers,
):
    response = client.post(
        "/budgets",
        json={
            "amount": 5000,
            "month": 8,
            "year": 2026,
            "category_id": 99999,
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 400


def test_cannot_access_other_users_budget(
    client,
):
    user1 = create_authenticated_user(client)

    user2 = create_authenticated_user(
        client,
        email="another@example.com",
    )

    category = create_user_category(
        client,
        user1,
    )

    budget = create_budget(
        client,
        user1.headers,
        category["id"],
    )

    response = client.put(
        f"/budgets/{budget['id']}",
        json={
            "amount": 9000,
        },
        headers=user2.headers,
    )

    assert response.status_code == 403


def test_budget_status(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    create_budget(
        client,
        authenticated_headers,
        category["id"],
        amount=1000,
    )

    response = client.get(
        "/budgets/status",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["category"] == category["name"]
    assert Decimal(body[0]["budget"]) == Decimal("1000.00")
    assert Decimal(body[0]["spent"]) == Decimal("0.00")
    assert Decimal(body[0]["remaining"]) == Decimal("1000.00")
    assert body[0]["percentage_used"] == 0
    assert body[0]["status"] == "Healthy"


def test_budget_status_with_expenses(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    create_budget(
        client,
        authenticated_headers,
        category["id"],
        amount=1000,
    )

    client.post(
        "/transactions",
        json={
            "amount": 500,
            "type": "expense",
            "description": "Groceries",
            "transaction_date": "2026-08-05",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    response = client.get(
        "/budgets/status",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert Decimal(body[0]["budget"]) == Decimal("1000.00")
    assert Decimal(body[0]["spent"]) == Decimal("500.00")
    assert Decimal(body[0]["remaining"]) == Decimal("500.00")
    assert body[0]["percentage_used"] == 50
    assert body[0]["status"] == "Healthy"


def test_budget_alerts_below_threshold(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    create_budget(
        client,
        authenticated_headers,
        category["id"],
        amount=1000,
    )

    client.post(
        "/transactions",
        json={
            "amount": 500,
            "type": "expense",
            "description": "Groceries",
            "transaction_date": "2026-08-05",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    response = client.get(
        "/budgets/alerts",
        headers=authenticated_headers,
    )

    assert response.status_code == 200
    assert response.json() == []


def test_budget_alert_warning(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    create_budget(
        client,
        authenticated_headers,
        category["id"],
        amount=1000,
    )

    client.post(
        "/transactions",
        json={
            "amount": 800,
            "type": "expense",
            "description": "Shopping",
            "transaction_date": "2026-08-05",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    response = client.get(
        "/budgets/alerts",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert Decimal(body[0]["budget"]) == Decimal("1000.00")
    assert Decimal(body[0]["spent"]) == Decimal("800.00")
    assert Decimal(body[0]["remaining"]) == Decimal("200.00")
    assert body[0]["percentage_used"] == 80
    assert body[0]["status"] == "Warning"


def test_budget_status_exceeded(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    create_budget(
        client,
        authenticated_headers,
        category["id"],
        amount=1000,
    )

    client.post(
        "/transactions",
        json={
            "amount": 1200,
            "type": "expense",
            "description": "Overspending",
            "transaction_date": "2026-08-05",
            "category_id": category["id"],
        },
        headers=authenticated_headers,
    )

    response = client.get(
        "/budgets/status",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert Decimal(body[0]["budget"]) == Decimal("1000.00")
    assert Decimal(body[0]["spent"]) == Decimal("1200.00")
    assert Decimal(body[0]["remaining"]) == Decimal("-200.00")
    assert body[0]["percentage_used"] == 120
    assert body[0]["status"] == "Exceeded"
