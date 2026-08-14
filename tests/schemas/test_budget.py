from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.budget import BudgetCreate, BudgetUpdate


def test_budget_create_accepts_valid_data():
    budget = BudgetCreate(
        amount=Decimal("25000.00"),
        month=8,
        year=2026,
        category_id=1,
    )

    assert budget.amount == Decimal("25000.00")
    assert budget.month == 8
    assert budget.year == 2026
    assert budget.category_id == 1


@pytest.mark.parametrize(
    "amount",
    [
        Decimal(0),
        Decimal("-100.00"),
    ],
)
def test_budget_create_rejects_non_positive_amount(amount):
    with pytest.raises(ValidationError):
        BudgetCreate(
            amount=amount,
            month=8,
            year=2026,
            category_id=1,
        )


@pytest.mark.parametrize(
    "month",
    [0, 13],
)
def test_budget_create_rejects_invalid_month(month):
    with pytest.raises(ValidationError):
        BudgetCreate(
            amount=Decimal("1000.00"),
            month=month,
            year=2026,
            category_id=1,
        )


@pytest.mark.parametrize(
    "year",
    [1999, 2101],
)
def test_budget_create_rejects_invalid_year(year):
    with pytest.raises(ValidationError):
        BudgetCreate(
            amount=Decimal("1000.00"),
            month=8,
            year=year,
            category_id=1,
        )


def test_budget_create_rejects_invalid_category_id():
    with pytest.raises(ValidationError):
        BudgetCreate(
            amount=Decimal("1000.00"),
            month=8,
            year=2026,
            category_id=0,
        )


def test_budget_update_allows_partial_updates():
    budget = BudgetUpdate(
        amount=Decimal("5000.00"),
    )

    assert budget.amount == Decimal("5000.00")
    assert budget.month is None
    assert budget.year is None
    assert budget.category_id is None


def test_budget_update_rejects_invalid_amount():
    with pytest.raises(ValidationError):
        BudgetUpdate(
            amount=Decimal(0),
        )


def test_budget_update_rejects_invalid_month():
    with pytest.raises(ValidationError):
        BudgetUpdate(
            month=13,
        )


def test_budget_update_rejects_invalid_category_id():
    with pytest.raises(ValidationError):
        BudgetUpdate(
            category_id=0,
        )
        