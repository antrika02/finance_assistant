from math import ceil

from pydantic import BaseModel


class PaginatedResponse[T](BaseModel):
    """
    Generic paginated response model.
    """

    items: list[T]
    page: int
    size: int
    total: int
    pages: int

    @classmethod
    def create(
        cls,
        *,
        items: list[T],
        page: int,
        size: int,
        total: int,
    ) -> "PaginatedResponse[T]":
        return cls(
            items=items,
            page=page,
            size=size,
            total=total,
            pages=ceil(total / size) if total else 0,
        )