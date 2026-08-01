from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.auth.dependencies import get_current_user
from app.dependencies.services import get_export_service
from app.models import User
from app.services.export_service import ExportService

router = APIRouter(
    prefix="/export",
    tags=["Export"],
)


@router.get("/csv")
def export_csv(
    current_user: User = Depends(get_current_user),
    service: ExportService = Depends(get_export_service),
):

    csv_data = service.export_transactions_csv(
        current_user.id
    )

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=transactions.csv"
        },
    )