from app.dependencies import (
    PaginationParams,
    TransactionSort,
)
from app.exceptions.base import AppException
from app.models import Transaction
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas import (
    PaginatedResponse,
    SummaryResponse,
    TransactionCreate,
    TransactionFilters,
    TransactionResponse,
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
    ) -> TransactionResponse:

        category = self.category_repository.get_by_id(
            data.category_id
        )

        if category is None:
            raise AppException("Category not found.")

        if category.user_id != user_id:
            raise AppException(
                "You cannot use another user's category."
            )

        transaction = self.repository.create(
            amount=data.amount,
            type=data.type,
            description=data.description,
            transaction_date=data.transaction_date,
            category_id=data.category_id,
            user_id=user_id,
        )

        return TransactionResponse.model_validate(transaction)

    def get_transactions(
        self,
        user_id: int,
        pagination: PaginationParams,
        filters: TransactionFilters,
        sort: TransactionSort,
    ) -> PaginatedResponse[TransactionResponse]:

        transactions = self.repository.get_by_user(
            user_id=user_id,
            offset=pagination.offset,
            limit=pagination.size,
            filters=filters,
            sort=sort,
        )

        total = self.repository.count_by_user(
            user_id=user_id,
            filters=filters,
        )

        items = [
            TransactionResponse.model_validate(transaction)
            for transaction in transactions
        ]

        return PaginatedResponse[TransactionResponse].create(
            items=items,
            page=pagination.page,
            size=pagination.size,
            total=total,
        )

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
    ) -> TransactionResponse:

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(transaction, key, value)

        transaction = self.repository.update(transaction)

        return TransactionResponse.model_validate(transaction)

    def delete_transaction(
        self,
        transaction: Transaction,
    ) -> None:
        self.repository.delete(transaction)

    def get_summary(
        self,
        user_id: int,
    ) -> SummaryResponse:

        income, expense = self.repository.get_summary(user_id)

        return SummaryResponse(
            total_income=income,
            total_expense=expense,
            balance=income - expense,
        )