from pydantic import BaseModel


class AIInsightResponse(BaseModel):
    insights: str