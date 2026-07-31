from app.exceptions.category import (
    CategoryAccessDeniedError,
    CategoryNotFoundError,
)
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def create_category(
        self,
        data: CategoryCreate,
        user_id: int,
    ) -> Category:
        return self.repository.create(
            name=data.name,
            type=data.type,
            icon=data.icon,
            color=data.color,
            user_id=user_id,
        )

    def get_categories(
        self,
        user_id: int,
    ) -> list[Category]:
        return self.repository.get_by_user(user_id)

    def get_owned_category(
        self,
        category_id: int,
        user_id: int,
    ) -> Category:
        category = self.repository.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError()

        if category.user_id != user_id:
            raise CategoryAccessDeniedError()

        return category

    def update_category(
        self,
        category: Category,
        data: CategoryUpdate,
    ) -> Category:
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(category, key, value)

        return self.repository.update(category)

    def delete_category(
        self,
        category: Category,
    ) -> None:
        self.repository.delete(category)