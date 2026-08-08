from decimal import Decimal

from pydantic import BaseModel


class MonthlyReportResponse(BaseModel):
    month: str
    income: Decimal
    expense: Decimal
    balance: Decimal
    savings_rate: float
