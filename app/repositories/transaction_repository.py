from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Transaction
from app.repositories.base_repository import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):

    def __init__(self, db: Session):
        super().__init__(db, Transaction)

    def get_by_user(
        self,
        user_id: int,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Transaction]:
        statement = (
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.transaction_date.desc())
            .offset(offset)
            .limit(limit)
        )

        result = self.db.execute(statement)

        return result.scalars().all()

    def count_by_user(
        self,
        user_id: int,
    ) -> int:
        statement = (
            select(func.count())
            .select_from(Transaction)
            .where(Transaction.user_id == user_id)
        )

        result = self.db.execute(statement)

        return result.scalar_one()