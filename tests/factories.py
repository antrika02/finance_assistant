from uuid import uuid4


def user_payload(
    full_name: str = "John Doe",
    email: str | None = None,
    password: str = "Password123!",
):
    """
    Returns a valid registration payload.
    """

    return {
        "full_name": full_name,
        "email": email or f"{uuid4().hex}@example.com",
        "password": password,
    }


def category_payload():
    return {
        "name": "Food",
        "type": "expense",
        "icon": "🍕",
        "color": "#FF5733",
    }


def transaction_payload(category_id: int):
    return {
        "amount": 250,
        "type": "expense",
        "description": "Lunch",
        "transaction_date": "2026-08-01",
        "category_id": category_id,
    }