from app.exceptions.base import AppException
from app.models import Category, Transaction
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas import (
    TransactionCreate,
    TransactionUpdate,
)


class TransactionNotFoundError(AppException):
    status_code = 404

    def __init__(self):
        super().__init__("Transaction not found.")


class TransactionAccessDeniedError(AppException):
    status_code = 403

    def __init__(self):
        super().__init__(
            "You do not have permission to access this transaction."
        )


class TransactionService:

    def __init__(
        self,
        repository: TransactionRepository,
        category_repository: CategoryRepository,
    ):
        self.repository = repository
        self.category_repository = category_repository

    def create_transaction(
        self,
        data: TransactionCreate,
        user_id: int,
    ) -> Transaction:

        category = self.category_repository.get_by_id(
            data.category_id
        )

        if category is None:
            raise AppException("Category not found.")

        if category.user_id != user_id:
            raise AppException(
                "You cannot use another user's category."
            )

        return self.repository.create(
            amount=data.amount,
            type=data.type,
            description=data.description,
            transaction_date=data.transaction_date,
            category_id=data.category_id,
            user_id=user_id,
        )

    def get_transactions(
        self,
        user_id: int,
    ) -> list[Transaction]:
        return self.repository.get_by_user(user_id)

    def get_owned_transaction(
        self,
        transaction_id: int,
        user_id: int,
    ) -> Transaction:

        transaction = self.repository.get_by_id(transaction_id)

        if transaction is None:
            raise TransactionNotFoundError()

        if transaction.user_id != user_id:
            raise TransactionAccessDeniedError()

        return transaction

    def update_transaction(
        self,
        transaction: Transaction,
        data: TransactionUpdate,
    ) -> Transaction:

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(transaction, key, value)

        return self.repository.update(transaction)

    def delete_transaction(
        self,
        transaction: Transaction,
    ) -> None:
        self.repository.delete(transaction)