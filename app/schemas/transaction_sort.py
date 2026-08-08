from pydantic import BaseModel


class TransactionSort(BaseModel):
    field: str = "transaction_date"
    descending: bool = True
