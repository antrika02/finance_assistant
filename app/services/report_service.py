from app.repositories.report_repository import ReportRepository
from app.schemas import MonthlyReportResponse


class ReportService:

    def __init__(
        self,
        repository: ReportRepository,
    ):
        self.repository = repository

    def monthly_report(
        self,
        user_id: int,
    ) -> list[MonthlyReportResponse]:

        result = self.repository.monthly_report(user_id)

        reports = []

        for row in result:

            savings_rate = (
                float((row.balance / row.income) * 100)
                if row.income
                else 0.0
            )

            reports.append(
                MonthlyReportResponse(
                    month=row.month,
                    income=row.income,
                    expense=row.expense,
                    balance=row.balance,
                    savings_rate=savings_rate,
                )
            )

        return reports