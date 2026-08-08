from tests.auth import create_category, create_transaction


def test_monthly_report(
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
        type="income",
        description="August Salary",
        transaction_date="2026-08-01",
    )

    create_transaction(
        client,
        authenticated_headers,
        category["id"],
        amount=2000,
        type="expense",
        description="August Rent",
        transaction_date="2026-08-05",
    )

    response = client.get(
        "/reports/monthly",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1

    report = body[0]

    assert report["month"] == "2026-08"
    assert report["income"] == "5000.00"
    assert report["expense"] == "2000.00"
    assert report["balance"] == "3000.00"
    assert report["savings_rate"] == 60.0


def test_monthly_report_multiple_months(
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
        type="income",
        description="August Salary",
        transaction_date="2026-08-01",
    )

    create_transaction(
        client,
        authenticated_headers,
        category["id"],
        amount=2000,
        type="expense",
        description="August Rent",
        transaction_date="2026-08-05",
    )

    create_transaction(
        client,
        authenticated_headers,
        category["id"],
        amount=4000,
        type="income",
        description="July Salary",
        transaction_date="2026-07-01",
    )

    create_transaction(
        client,
        authenticated_headers,
        category["id"],
        amount=1000,
        type="expense",
        description="July Rent",
        transaction_date="2026-07-05",
    )

    response = client.get(
        "/reports/monthly",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 2

    assert body[0]["month"] == "2026-07"

    assert body[0]["income"] == "4000.00"

    assert body[0]["expense"] == "1000.00"

    assert body[0]["balance"] == "3000.00"

    assert body[0]["savings_rate"] == 75.0

    assert body[1]["month"] == "2026-08"

    assert body[1]["income"] == "5000.00"

    assert body[1]["expense"] == "2000.00"

    assert body[1]["balance"] == "3000.00"

    assert body[1]["savings_rate"] == 60.0


def test_monthly_report_without_token(client):

    response = client.get("/reports/monthly")

    assert response.status_code == 401


def test_monthly_report_empty(
    client,
    authenticated_headers,
):

    response = client.get(
        "/reports/monthly",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    assert response.json() == []


def test_monthly_report_user_isolation(
    client,
):

    from tests.fixtures.categories import create_user_category
    from tests.fixtures.transactions import create_user_transaction
    from tests.fixtures.users import create_authenticated_user

    user1 = create_authenticated_user(client)

    user2 = create_authenticated_user(
        client,
        email="report-user-2@example.com",
    )

    category = create_user_category(
        client,
        user1,
    )

    create_user_transaction(
        client,
        user1,
        category["id"],
        amount=5000,
        type="income",
        description="User 1 Salary",
        transaction_date="2026-08-01",
    )

    response = client.get(
        "/reports/monthly",
        headers=user2.headers,
    )

    assert response.status_code == 200

    assert response.json() == []
