from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session):
        super().__init__(db, Category)

    def get_by_user(self, user_id: int) -> list[Category]:
        statement = (
            select(Category).where(Category.user_id == user_id).order_by(Category.name)
        )

        return list(self.db.scalars(statement).all())
