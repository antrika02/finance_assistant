from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.enums import TransactionType
from app.models import Transaction


class ReportRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def monthly_report(
        self,
        user_id: int,
    ):
        month = func.to_char(
            Transaction.transaction_date,
            "YYYY-MM",
        ).label("month")

        income = func.sum(
            case(
                (
                    Transaction.type == TransactionType.INCOME,
                    Transaction.amount,
                ),
                else_=0,
            )
        ).label("income")

        expense = func.sum(
            case(
                (
                    Transaction.type == TransactionType.EXPENSE,
                    Transaction.amount,
                ),
                else_=0,
            )
        ).label("expense")

        balance = (
            income - expense
        ).label("balance")

        statement = (
            select(
                month,
                income,
                expense,
                balance,
            )
            .where(
                Transaction.user_id == user_id,
            )
            .group_by(month)
            .order_by(month)
        )

        return self.db.execute(statement).all()