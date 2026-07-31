from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.enums import TransactionType
from app.models import Transaction


class DashboardRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_summary(
        self,
        user_id: int,
    ) -> dict:

        income = self.db.scalar(
            select(func.sum(Transaction.amount)).where(
                Transaction.user_id == user_id,
                Transaction.type == TransactionType.INCOME,
            )
        )

        expense = self.db.scalar(
            select(func.sum(Transaction.amount)).where(
                Transaction.user_id == user_id,
                Transaction.type == TransactionType.EXPENSE,
            )
        )

        total_transactions = self.db.scalar(
            select(func.count(Transaction.id)).where(
                Transaction.user_id == user_id,
            )
        )

        income = income or 0
        expense = expense or 0

        return {
            "total_income": income,
            "total_expense": expense,
            "current_balance": income - expense,
            "total_transactions": total_transactions or 0,
        }