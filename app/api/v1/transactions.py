from datetime import date

from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencies import get_current_user
from app.dependencies import PaginationParams, get_pagination
from app.dependencies.services import get_transaction_service
from app.enums import TransactionType
from app.models import User
from app.schemas import (
    PaginatedResponse,
    TransactionCreate,
    TransactionFilters,
    TransactionResponse,
    TransactionUpdate,
)
from app.services.transaction_service import TransactionService

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post(
    "",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    request: TransactionCreate,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    return service.create_transaction(
        request,
        current_user.id,
    )


@router.get(
    "",
    response_model=PaginatedResponse[TransactionResponse],
)
def get_transactions(
    current_user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(get_pagination),

    type: TransactionType | None = Query(default=None),
    category_id: int | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),

    service: TransactionService = Depends(get_transaction_service),
):

    filters = TransactionFilters(
        type=type,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date,
    )

    return service.get_transactions(
        current_user.id,
        pagination,
        filters,
    )


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    return service.get_transaction(
        transaction_id,
        current_user.id,
    )


@router.put(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def update_transaction(
    transaction_id: int,
    request: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    transaction = service.get_owned_transaction(
        transaction_id,
        current_user.id,
    )

    return service.update_transaction(
        transaction,
        request,
    )


@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    transaction = service.get_owned_transaction(
        transaction_id,
        current_user.id,
    )

    service.delete_transaction(transaction)