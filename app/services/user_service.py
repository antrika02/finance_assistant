from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.exceptions.user import UserAlreadyExistsError

class UserService:
    """
    Handles business logic for users.
    """

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, data: UserCreate) -> User:
        """
        Create a new user after validating business rules.
        """

        existing_user = self.repository.get_by_email(str(data.email))

        if existing_user:
            raise UserAlreadyExistsError(

                 "A user with this email already exists."

            )

        return self.repository.create(
            full_name=data.full_name,
            email=str(data.email),
        )
    
    def get_user(self, user_id: int) -> User | None:
        return self.repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        return self.repository.get_by_email(email)

    def get_all_users(self) -> list[User]:
        return self.repository.get_all()

    def delete_user(self, user_id: int) -> bool:
        user = self.repository.get_by_id(user_id)

        if user is None:
            return False

        self.repository.delete(user)
        return True

    