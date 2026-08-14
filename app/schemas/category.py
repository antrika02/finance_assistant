from pydantic import BaseModel, ConfigDict, Field

from app.enums import CategoryType


class CategoryCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )
    type: CategoryType
    icon: str = Field(
        min_length=1,
        max_length=50,
    )
    color: str = Field(
        min_length=1,
        max_length=20,
    )


class CategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    type: CategoryType | None = None
    icon: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )
    color: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )


class CategoryResponse(BaseModel):
    id: int
    name: str
    type: CategoryType
    icon: str
    color: str
    user_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )