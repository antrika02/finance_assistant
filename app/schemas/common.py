from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedResponse(GenericModel, Generic[T]):
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
    ):
        return cls(
            items=items,
            page=page,
            size=size,
            total=total,
            pages=ceil(total / size) if total else 0,
        )