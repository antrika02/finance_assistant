from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.enums import TransactionType
from app.models import Budget, Category, Transaction
from app.repositories.base_repository import BaseRepository


class BudgetRepository(BaseRepository[Budget]):

    def __init__(self, db: Session):
        super().__init__(db, Budget)

    def get_by_user(
        self,
        user_id: int,
    ) -> list[Budget]:
        statement = (
            select(Budget)
            .where(Budget.user_id == user_id)
            .order_by(
                Budget.year.desc(),
                Budget.month.desc(),
            )
        )

        return list(self.db.scalars(statement).all())

    def get_user_budget(
        self,
        budget_id: int,
        user_id: int,
    ) -> Budget | None:
        statement = select(Budget).where(
            Budget.id == budget_id,
            Budget.user_id == user_id,
        )

        return self.db.scalar(statement)

    def get_by_category_month(
        self,
        *,
        user_id: int,
        category_id: int,
        month: int,
        year: int,
    ) -> Budget | None:

        statement = select(Budget).where(
            Budget.user_id == user_id,
            Budget.category_id == category_id,
            Budget.month == month,
            Budget.year == year,
        )

        return self.db.scalar(statement)

    def get_budget_status(
        self,
        user_id: int,
    ):
        statement = (
            select(
                Category.name.label("category"),
                Budget.amount.label("budget"),
                func.coalesce(
                    func.sum(Transaction.amount),
                    0,
                ).label("spent"),
            )
            .join(
                Category,
                Budget.category_id == Category.id,
            )
            .outerjoin(
                Transaction,
                (Transaction.category_id == Budget.category_id)
                & (Transaction.user_id == Budget.user_id)
                & (Transaction.type == TransactionType.EXPENSE),
            )
            .where(
                Budget.user_id == user_id,
            )
            .group_by(
                Category.name,
                Budget.amount,
            )
        )

        return self.db.execute(statement).all()

    def get_alerts(
        self,
        user_id: int,
    ):
        return self.get_budget_status(user_id)