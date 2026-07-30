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

    def get_category(
        self,
        category_id: int,
    ) -> Category | None:
        return self.repository.get_by_id(category_id)

    def update_category(
        self,
        category: Category,
        data: CategoryUpdate,
    ) -> Category:
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(category, key, value)

        self.repository.db.commit()
        self.repository.db.refresh(category)

        return category

    def delete_category(
        self,
        category: Category,
    ) -> None:
        self.repository.delete(category)