from app.ai.client import GeminiClient
from app.ai.prompt_builder import PromptBuilder
from app.services.dashboard_service import DashboardService
from app.services.budget_service import BudgetService


class ChatService:

    def __init__(
        self,
        dashboard_service: DashboardService,
        budget_service: BudgetService,
    ):
        self.dashboard_service = dashboard_service
        self.budget_service = budget_service
        self.client = GeminiClient()

    def chat(
        self,
        *,
        user_id: int,
        message: str,
    ) -> str:

        summary = self.dashboard_service.get_summary(
            user_id
        )

        budgets = self.budget_service.get_budget_status(
            user_id
        )

        top_categories = (
            self.dashboard_service.get_top_spending_categories(
                user_id
            )
        )

        prompt = PromptBuilder.build_chat_prompt(
            message=message,
            summary=summary,
            budgets=budgets,
            top_categories=top_categories,
        )

        return self.client.generate(prompt)