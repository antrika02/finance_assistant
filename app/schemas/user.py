from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """
    Request schema for creating a user.
    """

    full_name: str
    email: EmailStr


class UserUpdate(BaseModel):
    """
    Request schema for updating a user.
    """

    full_name: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):
    """
    Response schema returned to clients.
    """

    id: int
    full_name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
