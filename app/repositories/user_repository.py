from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for user-specific database operations.
    """

    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by email.
        """
        statement = select(User).where(User.email == email)

        return self.db.scalar(statement)
