from io import BytesIO

from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet

from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.transaction_repository import (
    TransactionRepository,
)


class PDFService:

    def __init__(
        self,
        dashboard_repository: DashboardRepository,
        transaction_repository: TransactionRepository,
    ):
        self.dashboard_repository = dashboard_repository
        self.transaction_repository = transaction_repository

    def generate_report(
        self,
        user_id: int,
    ) -> bytes:

        summary = self.dashboard_repository.get_summary(user_id)

        transactions = self.transaction_repository.get_by_user(
            user_id=user_id,
            offset=0,
            limit=10,
            filters=None,
            sort=None,
        )

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
        )

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b>Personal Finance Report</b>",
                styles["Title"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                f"Total Income : {summary['total_income']}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Total Expense : {summary['total_expense']}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Balance : {summary['current_balance']}",
                styles["BodyText"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Recent Transactions</b>",
                styles["Heading2"],
            )
        )

        for transaction in transactions:

            story.append(
                Paragraph(
                    f"{transaction.transaction_date} | "
                    f"{transaction.category.name} | "
                    f"{transaction.type.value} | "
                    f"{transaction.amount}",
                    styles["BodyText"],
                )
            )

        document.build(story)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf