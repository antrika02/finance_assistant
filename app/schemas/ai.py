from pydantic import BaseModel


class AIInsightResponse(BaseModel):
    insights: str


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str