from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.dependencies.services import get_dashboard_service
from app.models import User
from app.schemas.dashboard import (
    CategoryBreakdownResponse,
    DashboardSummaryResponse,
    MonthlySummaryResponse,
    RecentTransactionResponse,
)
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
)
def get_summary(
    current_user: User = Depends(get_current_user),
    service: DashboardService = Depends(get_dashboard_service),
):
    return service.get_summary(current_user.id)


@router.get(
    "/category-breakdown",
    response_model=list[CategoryBreakdownResponse],
)
def get_category_breakdown(
    current_user: User = Depends(get_current_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service),
):
    return dashboard_service.get_category_breakdown(current_user.id)


@router.get(
    "/monthly-summary",
    response_model=list[MonthlySummaryResponse],
)
def get_monthly_summary(
    current_user: User = Depends(get_current_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service),
):
    return dashboard_service.get_monthly_summary(current_user.id)


@router.get(
    "/recent-transactions",
    response_model=list[RecentTransactionResponse],
)
def get_recent_transactions(
    current_user: User = Depends(get_current_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service),
):
    return dashboard_service.get_recent_transactions(current_user.id)


@router.get(
    "/top-spending-categories",
    response_model=list[CategoryBreakdownResponse],
)
def get_top_spending_categories(
    current_user: User = Depends(get_current_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service),
):
    return dashboard_service.get_top_spending_categories(current_user.id)
