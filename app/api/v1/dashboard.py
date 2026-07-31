from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.dependencies.services import get_dashboard_service
from app.models import User
from app.schemas import DashboardSummaryResponse
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