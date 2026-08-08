from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.auth.dependencies import get_current_user
from app.dependencies.services import get_pdf_service
from app.models import User
from app.services.pdf_service import PDFService

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"],
)


@router.get("/report")
def download_pdf(
    current_user: User = Depends(get_current_user),
    service: PDFService = Depends(get_pdf_service),
):

    pdf = service.generate_report(current_user.id)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=finance_report.pdf"},
    )
