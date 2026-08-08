from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.services import get_user_service
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    """
    Create a new user.
    """
    return service.create_user(user)


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_all_users(
    service: UserService = Depends(get_user_service),
):
    """
    Retrieve all users.
    """
    return service.get_all_users()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    """
    Retrieve a user by ID.
    """
    user = service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user
