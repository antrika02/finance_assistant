from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.enums import TransactionType


class TransactionCreate(BaseModel):
    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )
    type: TransactionType
    description: str | None = Field(
        default=None,
        max_length=255,
    )
    transaction_date: date
    category_id: int = Field(
        gt=0,
    )


class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )
    type: TransactionType | None = None
    description: str | None = Field(
        default=None,
        max_length=255,
    )
    transaction_date: date | None = None
    category_id: int | None = Field(
        default=None,
        gt=0,
    )


class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    type: TransactionType
    description: str | None
    transaction_date: date
    category_id: int
    user_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )