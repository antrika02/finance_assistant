from app.auth.hashing import hash_password, verify_password
from app.exceptions.user import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest


class AuthService:
    def __init__(self, repository: UserRepository):
        self.user_repository = repository

    def register(
        self,
        request: RegisterRequest,
    ) -> User:
        existing_user = self.user_repository.get_by_email(request.email)

        if existing_user:
            raise UserAlreadyExistsError()

        return self.user_repository.create(
            full_name=request.full_name,
            email=request.email,
            hashed_password=hash_password(request.password),
            is_active=True,
            is_verified=False,
        )

    def authenticate(
        self,
        email: str,
        password: str,
    ) -> User:
        user = self.user_repository.get_by_email(email)

        if not user:
            raise UserNotFoundError()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        return user
