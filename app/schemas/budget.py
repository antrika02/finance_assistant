from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BudgetBase(BaseModel):
    amount: Decimal
    month: int
    year: int
    category_id: int


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    amount: Decimal | None = None
    month: int | None = None
    year: int | None = None
    category_id: int | None = None


class BudgetResponse(BudgetBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class BudgetStatusResponse(BaseModel):
    category: str
    budget: Decimal
    spent: Decimal
    remaining: Decimal
    percentage_used: float