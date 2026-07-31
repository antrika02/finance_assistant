from decimal import Decimal

from pydantic import BaseModel
from datetime import date

from app.enums import TransactionType

class DashboardSummaryResponse(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    current_balance: Decimal
    total_transactions: int

class CategoryBreakdownResponse(BaseModel):
    category: str
    amount: Decimal


class MonthlySummaryResponse(BaseModel):
    month: str
    income: Decimal
    expense: Decimal
    balance: Decimal

class RecentTransactionResponse(BaseModel):
    id: int
    description: str | None
    amount: Decimal
    type: TransactionType
    transaction_date: date
    category: str