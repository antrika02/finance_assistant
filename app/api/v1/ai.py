from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.dependencies.services import get_insight_service
from app.models import User
from app.schemas import AIInsightResponse
from app.services.insight_service import InsightService

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.get(
    "/insights",
    response_model=AIInsightResponse,
)
def get_ai_insights(
    current_user: User = Depends(get_current_user),
    service: InsightService = Depends(
        get_insight_service,
    ),
):
    return AIInsightResponse(
        insights=service.generate_insights(
            current_user.id
        )
    )