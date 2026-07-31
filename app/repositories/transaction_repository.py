from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Transaction
from app.repositories.base_repository import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):

    def __init__(self, db: Session):
        super().__init__(db, Transaction)

    def get_by_user(
        self,
        user_id: int,
    ) -> list[Transaction]:
        statement = (
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.transaction_date.desc())
        )

        return list(self.db.scalars(statement).all())