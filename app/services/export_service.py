import csv
from io import StringIO

from app.repositories.transaction_repository import TransactionRepository


class ExportService:
    def __init__(
        self,
        repository: TransactionRepository,
    ):
        self.repository = repository

    def export_transactions_csv(
        self,
        user_id: int,
    ) -> str:

        transactions = self.repository.get_by_user(
            user_id=user_id,
            offset=0,
            limit=100000,
            filters=None,
            sort=None,
        )

        output = StringIO()

        writer = csv.writer(output)

        writer.writerow(
            [
                "Date",
                "Category",
                "Type",
                "Amount",
                "Description",
            ]
        )

        for transaction in transactions:
            writer.writerow(
                [
                    transaction.transaction_date,
                    transaction.category.name,
                    transaction.type.value,
                    transaction.amount,
                    transaction.description,
                ]
            )

        return output.getvalue()
