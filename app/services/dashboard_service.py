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