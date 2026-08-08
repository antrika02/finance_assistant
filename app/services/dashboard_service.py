from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.dashboard import (
    CategoryBreakdownResponse,
    MonthlySummaryResponse,
    RecentTransactionResponse,
)


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
            CategoryBreakdownResponse(
                category=row.category,
                amount=row.amount,
            )
            for row in result
        ]

    def get_monthly_summary(self, user_id: int):
        result = self.repository.get_monthly_summary(user_id)

        return [
            MonthlySummaryResponse(
                month=f"{int(row.year):04d}-{int(row.month):02d}",
                income=row.income,
                expense=row.expense,
                balance=row.balance,
            )
            for row in result
        ]

    def get_recent_transactions(self, user_id: int):
        result = self.repository.get_recent_transactions(user_id)

        return [
            RecentTransactionResponse(
                id=row.id,
                description=row.description,
                amount=row.amount,
                type=row.type,
                transaction_date=row.transaction_date,
                category=row.category,
            )
            for row in result
        ]

    def get_top_spending_categories(self, user_id: int):
        result = self.repository.get_category_breakdown(
            user_id=user_id,
            limit=5,
        )

        return [
            CategoryBreakdownResponse(
                category=row.category,
                amount=row.amount,
            )
            for row in result
        ]
