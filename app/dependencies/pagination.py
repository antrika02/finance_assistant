from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int
    size: int

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


def get_pagination(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    size: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Items per page",
    ),
) -> PaginationParams:
    return PaginationParams(
        page=page,
        size=size,
    )
