from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.enums import TransactionType
from app.schemas.transaction import TransactionCreate, TransactionUpdate


def test_transaction_create_accepts_valid_data():
    transaction = TransactionCreate(
        amount=Decimal("1250.50"),
        type=TransactionType.EXPENSE,
        description="Groceries",
        transaction_date=date(2026, 8, 14),
        category_id=1,
    )

    assert transaction.amount == Decimal("1250.50")
    assert transaction.type == TransactionType.EXPENSE
    assert transaction.description == "Groceries"
    assert transaction.transaction_date == date(2026, 8, 14)
    assert transaction.category_id == 1


@pytest.mark.parametrize(
    "amount",
    [
        Decimal(0),
        Decimal("-100.00"),
    ],
)
def test_transaction_create_rejects_non_positive_amount(amount):
    with pytest.raises(ValidationError):
        TransactionCreate(
            amount=amount,
            type=TransactionType.EXPENSE,
            description="Groceries",
            transaction_date=date(2026, 8, 14),
            category_id=1,
        )


def test_transaction_create_rejects_invalid_category_id():
    with pytest.raises(ValidationError):
        TransactionCreate(
            amount=Decimal("100.00"),
            type=TransactionType.EXPENSE,
            description="Groceries",
            transaction_date=date(2026, 8, 14),
            category_id=0,
        )


def test_transaction_create_allows_optional_description():
    transaction = TransactionCreate(
        amount=Decimal("500.00"),
        type=TransactionType.INCOME,
        transaction_date=date(2026, 8, 14),
        category_id=1,
    )

    assert transaction.description is None


def test_transaction_create_rejects_long_description():
    with pytest.raises(ValidationError):
        TransactionCreate(
            amount=Decimal("500.00"),
            type=TransactionType.EXPENSE,
            description="x" * 256,
            transaction_date=date(2026, 8, 14),
            category_id=1,
        )


def test_transaction_update_allows_partial_updates():
    transaction = TransactionUpdate(
        amount=Decimal("2500.00"),
    )

    assert transaction.amount == Decimal("2500.00")
    assert transaction.type is None
    assert transaction.description is None
    assert transaction.transaction_date is None
    assert transaction.category_id is None


def test_transaction_update_rejects_non_positive_amount():
    with pytest.raises(ValidationError):
        TransactionUpdate(
            amount=Decimal(0),
        )


def test_transaction_update_rejects_invalid_category_id():
    with pytest.raises(ValidationError):
        TransactionUpdate(
            category_id=0,
        )


def test_transaction_update_rejects_long_description():
    with pytest.raises(ValidationError):
        TransactionUpdate(
            description="x" * 256,
        )