from uuid import uuid4


def user_payload(
    full_name: str = "John Doe",
    email: str | None = None,
    password: str = "Password123!",
):
    return {
        "full_name": full_name,
        "email": email or f"{uuid4().hex}@example.com",
        "password": password,
    }


def category_payload(
    name="Food",
    type="expense",
    icon="🍕",
    color="#FF5733",
):
    return {
        "name": name,
        "type": type,
        "icon": icon,
        "color": color,
    }


def transaction_payload(
    category_id: int,
    amount=250,
    type="expense",
    description="Lunch",
    transaction_date="2026-08-01",
):
    return {
        "amount": amount,
        "type": type,
        "description": description,
        "transaction_date": transaction_date,
        "category_id": category_id,
    }
