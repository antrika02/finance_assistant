from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BudgetBase(BaseModel):
    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )
    month: int = Field(
        ge=1,
        le=12,
    )
    year: int = Field(
        ge=2000,
        le=2100,
    )
    category_id: int = Field(
        gt=0,
    )


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    amount: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )
    month: int | None = Field(
        default=None,
        ge=1,
        le=12,
    )
    year: int | None = Field(
        default=None,
        ge=2000,
        le=2100,
    )
    category_id: int | None = Field(
        default=None,
        gt=0,
    )


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
    status: str