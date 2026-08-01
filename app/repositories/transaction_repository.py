from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.models import Transaction
from app.repositories.base_repository import BaseRepository
from app.schemas import TransactionFilters, TransactionSort


class TransactionRepository(BaseRepository[Transaction]):

    def __init__(self, db: Session):
        super().__init__(db, Transaction)

    def get_by_user(
        self,
        user_id: int,
        offset: int = 0,
        limit: int = 20,
        filters: TransactionFilters | None = None,
        sort: TransactionSort | None = None,
    ) -> list[Transaction]:

        statement = (
            select(Transaction)
            .where(Transaction.user_id == user_id)
        )

        # Apply Filters

        if filters:

            if filters.type:
                statement = statement.where(
                    Transaction.type == filters.type
                )

            if filters.category_id:
                statement = statement.where(
                    Transaction.category_id == filters.category_id
                )

            if filters.start_date:
                statement = statement.where(
                    Transaction.transaction_date >= filters.start_date
                )

            if filters.end_date:
                statement = statement.where(
                    Transaction.transaction_date <= filters.end_date
                )

        # Apply Sorting
        if sort:

            sort_column = getattr(
                Transaction,
                sort.field,
                Transaction.transaction_date,
            )

            if sort.descending:
                statement = statement.order_by(
                    desc(sort_column)
                )
            else:
                statement = statement.order_by(
                    asc(sort_column)
                )

        else:

            statement = statement.order_by(
                Transaction.transaction_date.desc()
            )

        # Apply Pagination

        statement = (
            statement
            .offset(offset)
            .limit(limit)
        )

        result = self.db.execute(statement)

        return result.scalars().all()

    def count_by_user(
        self,
        user_id: int,
        filters: TransactionFilters | None = None,
    ) -> int:

        statement = (
            select(func.count())
            .select_from(Transaction)
            .where(Transaction.user_id == user_id)
        )
        # Apply Filters

        if filters:

            if filters.type:
                statement = statement.where(
                    Transaction.type == filters.type
                )

            if filters.category_id:
                statement = statement.where(
                    Transaction.category_id == filters.category_id
                )

            if filters.start_date:
                statement = statement.where(
                    Transaction.transaction_date >= filters.start_date
                )

            if filters.end_date:
                statement = statement.where(
                    Transaction.transaction_date <= filters.end_date
                )

        result = self.db.execute(statement)

        return result.scalar_one()