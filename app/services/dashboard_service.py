from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(
        self,
        repository: DashboardRepository,
    ):
        self.repository = repository

    def get_summary(
        self,
        user_id: int,
    ):
        return self.repository.get_summary(user_id)

    def get_category_breakdown(self, user_id: int):
        result = self.repository.get_category_breakdown(user_id)

        return [
            {
                "category": row.category,
                "amount": row.amount,
            }
            for row in result
        ]