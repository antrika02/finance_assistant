from app.ai.client import GeminiClient
from app.ai.prompt_builder import PromptBuilder
from app.services.budget_service import BudgetService
from app.services.dashboard_service import DashboardService


class InsightService:

    def __init__(
        self,
        dashboard_service: DashboardService,
        budget_service: BudgetService,
    ):
        self.dashboard_service = dashboard_service
        self.budget_service = budget_service
        self.client = GeminiClient()

    def generate_insights(
        self,
        user_id: int,
    ) -> str:

        summary = self.dashboard_service.get_summary(user_id)

        budgets = self.budget_service.get_budget_status(user_id)

        categories = self.dashboard_service.get_top_spending_categories(
            user_id
        )

        prompt = PromptBuilder.build_insight_prompt(
            summary,
            budgets,
            categories,
        )

        return self.client.generate(prompt)