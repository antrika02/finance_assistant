from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.dependencies.services import get_category_service
from app.models.user import User
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    request: CategoryCreate,
    current_user: User = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
):
    return service.create_category(
        data=request,
        user_id=current_user.id,
    )


@router.get(
    "/",
    response_model=list[CategoryResponse],
)
def get_categories(
    current_user: User = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
):
    return service.get_categories(current_user.id)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
):
    return service.get_owned_category(
        category_id,
        current_user.id,
    )


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    request: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
):
    category = service.get_owned_category(
        category_id,
        current_user.id,
    )

    return service.update_category(
        category,
        request,
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
):
    category = service.get_owned_category(
        category_id,
        current_user.id,
    )

    service.delete_category(category)
