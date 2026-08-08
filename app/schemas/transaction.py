from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.enums import TransactionType


class TransactionCreate(BaseModel):
    amount: Decimal
    type: TransactionType
    description: str | None = None
    transaction_date: date
    category_id: int


class TransactionUpdate(BaseModel):
    amount: Decimal | None = None
    type: TransactionType | None = None
    description: str | None = None
    transaction_date: date | None = None
    category_id: int | None = None


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
