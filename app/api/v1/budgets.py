from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.dependencies.services import get_budget_service
from app.models import User
from app.schemas import (
    BudgetCreate,
    BudgetResponse,
    BudgetStatusResponse,
    BudgetUpdate,
)
from app.services.budget_service import BudgetService

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"],
)


@router.post(
    "",
    response_model=BudgetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_budget(
    request: BudgetCreate,
    current_user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
):
    return service.create_budget(
        request,
        current_user.id,
    )


@router.get(
    "",
    response_model=list[BudgetResponse],
)
def get_budgets(
    current_user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
):
    return service.get_budgets(
        current_user.id,
    )


@router.get(
    "/status",
    response_model=list[BudgetStatusResponse],
)
def get_budget_status(
    current_user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
):
    return service.get_budget_status(
        current_user.id,
    )


@router.get(
    "/{budget_id}",
    response_model=BudgetResponse,
)
def get_budget(
    budget_id: int,
    current_user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
):
    return service.get_owned_budget(
        budget_id,
        current_user.id,
    )


@router.put(
    "/{budget_id}",
    response_model=BudgetResponse,
)
def update_budget(
    budget_id: int,
    request: BudgetUpdate,
    current_user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
):
    budget = service.get_owned_budget(
        budget_id,
        current_user.id,
    )

    return service.update_budget(
        budget,
        request,
    )


@router.delete(
    "/{budget_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_budget(
    budget_id: int,
    current_user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
):
    budget = service.get_owned_budget(
        budget_id,
        current_user.id,
    )

    service.delete_budget(budget)