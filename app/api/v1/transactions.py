from datetime import date

from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencies import get_current_user
from app.dependencies import PaginationParams
from app.dependencies.services import get_transaction_service
from app.models import User
from app.schemas import (
    PaginatedResponse,
    TransactionCreate,
    TransactionFilters,
    TransactionResponse,
    TransactionSort,
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
    type: str | None = Query(default=None),
    category_id: int | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    sort: str = Query(default="-transaction_date"),
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    filters = TransactionFilters(
        type=type,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date,
        search=search,
    )

    descending = sort.startswith("-")
    field = sort[1:] if descending else sort

    sort_params = TransactionSort(
        field=field,
        descending=descending,
    )

    pagination = PaginationParams(
        page=page,
        size=size,
    )

    return service.get_transactions(
        user_id=current_user.id,
        pagination=pagination,
        filters=filters,
        sort=sort_params,
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
    return service.get_owned_transaction(
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