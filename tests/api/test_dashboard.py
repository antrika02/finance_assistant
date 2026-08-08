from decimal import Decimal

from tests.auth import create_category


def create_transaction(
    client,
    headers,
    category_id,
    *,
    amount,
    transaction_type,
    description,
    transaction_date,
):
    response = client.post(
        "/transactions/",
        json={
            "amount": amount,
            "type": transaction_type,
            "description": description,
            "transaction_date": transaction_date,
            "category_id": category_id,
        },
        headers=headers,
    )

    assert response.status_code == 201

    return response.json()


def test_dashboard_summary_empty(
    client,
    authenticated_headers,
):
    response = client.get(
        "/dashboard/summary",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert Decimal(body["total_income"]) == Decimal("0")
    assert Decimal(body["total_expense"]) == Decimal("0")
    assert Decimal(body["current_balance"]) == Decimal("0")
    assert body["total_transactions"] == 0


def test_dashboard_summary(
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
        amount=5000,
        transaction_type="income",
        description="Salary",
        transaction_date="2026-08-01",
    )

    create_transaction(
        client,
        authenticated_headers,
        category["id"],
        amount=1500,
        transaction_type="expense",
        description="Rent",
        transaction_date="2026-08-02",
    )

    create_transaction(
        client,
        authenticated_headers,
        category["id"],
        amount=500,
        transaction_type="expense",
        description="Food",
        transaction_date="2026-08-03",
    )

    response = client.get(
        "/dashboard/summary",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert Decimal(body["total_income"]) == Decimal("5000")
    assert Decimal(body["total_expense"]) == Decimal("2000")
    assert Decimal(body["current_balance"]) == Decimal("3000")
    assert body["total_transactions"] == 3


def test_dashboard_category_breakdown(
    client,
    authenticated_headers,
):
    food = create_category(
        client,
        authenticated_headers,
    )

    travel_response = client.post(
        "/categories/",
        json={
            "name": "Travel",
            "type": "expense",
            "icon": "✈️",
            "color": "#0000FF",
        },
        headers=authenticated_headers,
    )

    assert travel_response.status_code == 201

    travel = travel_response.json()

    create_transaction(
        client,
        authenticated_headers,
        food["id"],
        amount=500,
        transaction_type="expense",
        description="Groceries",
        transaction_date="2026-08-01",
    )

    create_transaction(
        client,
        authenticated_headers,
        food["id"],
        amount=300,
        transaction_type="expense",
        description="Restaurant",
        transaction_date="2026-08-02",
    )

    create_transaction(
        client,
        authenticated_headers,
        travel["id"],
        amount=1000,
        transaction_type="expense",
        description="Flight",
        transaction_date="2026-08-03",
    )

    response = client.get(
        "/dashboard/category-breakdown",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 2

    assert body[0]["category"] == "Travel"
    assert Decimal(body[0]["amount"]) == Decimal("1000")

    assert body[1]["category"] == "Food"
    assert Decimal(body[1]["amount"]) == Decimal("800")


def test_dashboard_category_breakdown_excludes_income(
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
        amount=5000,
        transaction_type="income",
        description="Salary",
        transaction_date="2026-08-01",
    )

    create_transaction(
        client,
        authenticated_headers,
        category["id"],
        amount=500,
        transaction_type="expense",
        description="Food",
        transaction_date="2026-08-02",
    )

    response = client.get(
        "/dashboard/category-breakdown",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert Decimal(body[0]["amount"]) == Decimal("500")


def test_dashboard_monthly_summary(
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
        amount=5000,
        transaction_type="income",
        description="August Salary",
        transaction_date="2026-08-01",
    )

    create_transaction(
        client,
        authenticated_headers,
        category["id"],
        amount=2000,
        transaction_type="expense",
        description="August Rent",
        transaction_date="2026-08-05",
    )

    create_transaction(
        client,
        authenticated_headers,
        category["id"],
        amount=3000,
        transaction_type="income",
        description="July Salary",
        transaction_date="2026-07-01",
    )

    create_transaction(
        client,
        authenticated_headers,
        category["id"],
        amount=1000,
        transaction_type="expense",
        description="July Rent",
        transaction_date="2026-07-05",
    )

    response = client.get(
        "/dashboard/monthly-summary",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 2

    assert body[0]["month"] == "2026-07"
    assert Decimal(body[0]["income"]) == Decimal("3000")
    assert Decimal(body[0]["expense"]) == Decimal("1000")
    assert Decimal(body[0]["balance"]) == Decimal("2000")

    assert body[1]["month"] == "2026-08"
    assert Decimal(body[1]["income"]) == Decimal("5000")
    assert Decimal(body[1]["expense"]) == Decimal("2000")
    assert Decimal(body[1]["balance"]) == Decimal("3000")


def test_dashboard_recent_transactions(
    client,
    authenticated_headers,
):
    category = create_category(
        client,
        authenticated_headers,
    )

    for i in range(7):
        create_transaction(
            client,
            authenticated_headers,
            category["id"],
            amount=i + 1,
            transaction_type="expense",
            description=f"Transaction {i}",
            transaction_date=f"2026-08-{i + 1:02d}",
        )

    response = client.get(
        "/dashboard/recent-transactions",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 5

    assert body[0]["description"] == "Transaction 6"
    assert body[1]["description"] == "Transaction 5"
    assert body[4]["description"] == "Transaction 2"


def test_dashboard_top_spending_categories(
    client,
    authenticated_headers,
):
    categories = []

    for i in range(6):
        response = client.post(
            "/categories/",
            json={
                "name": f"Category {i}",
                "type": "expense",
                "icon": "💰",
                "color": "#000000",
            },
            headers=authenticated_headers,
        )

        assert response.status_code == 201

        categories.append(response.json())

    amounts = [100, 200, 300, 400, 500, 600]

    for category, amount in zip(categories, amounts):
        create_transaction(
            client,
            authenticated_headers,
            category["id"],
            amount=amount,
            transaction_type="expense",
            description=f"Expense {amount}",
            transaction_date="2026-08-01",
        )

    response = client.get(
        "/dashboard/top-spending-categories",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 5

    returned_amounts = [
        Decimal(item["amount"])
        for item in body
    ]

    assert returned_amounts == [
        Decimal("600"),
        Decimal("500"),
        Decimal("400"),
        Decimal("300"),
        Decimal("200"),
    ]


def test_dashboard_requires_authentication(client):
    endpoints = [
        "/dashboard/summary",
        "/dashboard/category-breakdown",
        "/dashboard/monthly-summary",
        "/dashboard/recent-transactions",
        "/dashboard/top-spending-categories",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)

        assert response.status_code == 401