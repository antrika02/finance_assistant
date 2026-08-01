from datetime import date

from pydantic import BaseModel

from app.enums import TransactionType


class TransactionFilters(BaseModel):
    type: TransactionType | None = None
    category_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None