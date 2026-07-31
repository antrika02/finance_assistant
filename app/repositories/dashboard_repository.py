from sqlalchemy import select, func, desc, case 
from sqlalchemy.orm import Session

from app.enums import TransactionType
from app.models import Category, Transaction


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

    def get_category_breakdown(self, user_id: int):
        statement = (
            select(
                Category.name.label("category"),
                func.sum(Transaction.amount).label("amount"),
            )
            .join(
                Transaction,
                Transaction.category_id == Category.id,
            )
            .where(
                Transaction.user_id == user_id,
                Transaction.type == TransactionType.EXPENSE,
            )
            .group_by(Category.name)
            .order_by(desc("amount"))
        )

        result = self.db.execute(statement)

        return result.all()

    def get_monthly_summary(self, user_id: int):

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

        from sqlalchemy import select, func, desc, case 
from sqlalchemy.orm import Session

from app.enums import TransactionType
from app.models import Category, Transaction


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

    def get_category_breakdown(self, user_id: int):
        statement = (
            select(
                Category.name.label("category"),
                func.sum(Transaction.amount).label("amount"),
            )
            .join(
                Transaction,
                Transaction.category_id == Category.id,
            )
            .where(
                Transaction.user_id == user_id,
                Transaction.type == TransactionType.EXPENSE,
            )
            .group_by(Category.name)
            .order_by(desc("amount"))
        )

        result = self.db.execute(statement)

        return result.all()

    def get_monthly_summary(self, user_id: int):

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

        result = self.db.execute(statement)

        return result.all()

    def get_recent_transactions(self, user_id: int):

        statement = (
            select(
                Transaction.id,
                Transaction.description,
                Transaction.amount,
                Transaction.type,
                Transaction.transaction_date,
                Category.name.label("category"),
            )
            .join(
                Category,
                Transaction.category_id == Category.id,
            )
            .where(
                Transaction.user_id == user_id,
            )
            .order_by(
                Transaction.transaction_date.desc()
            )
            .limit(5)
        )

        result = self.db.execute(statement)

        return result.all()