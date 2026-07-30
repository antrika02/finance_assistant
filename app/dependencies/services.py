from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.auth_service import AuthService

def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    """
    Returns a UserService instance.
    """
    repository = UserRepository(db)

    return UserService(repository)

def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    """
    Returns an AuthService instance.
    """
    repository = UserRepository(db)

    return AuthService(repository)