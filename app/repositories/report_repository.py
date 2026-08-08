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
        year = func.extract(
            "year",
            Transaction.transaction_date,
        ).label("year")

        month_number = func.extract(
            "month",
            Transaction.transaction_date,
        ).label("month_number")

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
                year,
                month_number,
                income,
                expense,
                balance,
            )
            .where(
                Transaction.user_id == user_id,
            )
            .group_by(
                year,
                month_number,
            )
            .order_by(
                year,
                month_number,
            )
        )

        return self.db.execute(statement).all()