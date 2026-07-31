from decimal import Decimal

from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    current_balance: Decimal
    total_transactions: int