from decimal import Decimal

from pydantic import BaseModel


class SummaryResponse(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
