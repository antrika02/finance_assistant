from pydantic import BaseModel


class TransactionSort(BaseModel):
    field: str
    descending: bool = False
