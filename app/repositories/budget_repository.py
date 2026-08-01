from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Budget
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