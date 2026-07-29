from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Handles all database operations for User.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, full_name: str, email: str) -> User:
        """
        Create a new user.
        """
        user = User(
            full_name=full_name,
            email=email,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by ID.
        """
        statement = select(User).where(User.id == user_id)

        return self.db.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by email.
        """
        statement = select(User).where(User.email == email)

        return self.db.scalar(statement)

    def get_all(self) -> list[User]:
        """
        Retrieve all users.
        """
        statement = select(User)

        return list(self.db.scalars(statement).all())

    def delete(self, user: User) -> None:
        """
        Delete a user.
        """
        self.db.delete(user)
        self.db.commit()