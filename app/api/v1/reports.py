from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.dependencies.services import get_report_service
from app.models import User
from app.schemas import MonthlyReportResponse
from app.services.report_service import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get(
    "/monthly",
    response_model=list[MonthlyReportResponse],
)
def get_monthly_report(
    current_user: User = Depends(get_current_user),
    service: ReportService = Depends(get_report_service),
):
    return service.monthly_report(current_user.id)