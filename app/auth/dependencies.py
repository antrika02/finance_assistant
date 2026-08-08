from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth.jwt import decode_access_token
from app.dependencies.services import get_user_service
from app.models.user import User
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
) -> User:
    payload = decode_access_token(token)

    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

    user = service.get_user_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    return user
