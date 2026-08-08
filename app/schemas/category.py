from pydantic import BaseModel, ConfigDict

from app.enums import CategoryType


class CategoryCreate(BaseModel):
    name: str
    type: CategoryType
    icon: str
    color: str


class CategoryUpdate(BaseModel):
    name: str | None = None
    type: CategoryType | None = None
    icon: str | None = None
    color: str | None = None


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
