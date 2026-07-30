from fastapi import status

from app.exceptions.base import AppException


class UserAlreadyExistsError(AppException):
    status_code = status.HTTP_409_CONFLICT


class UserNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND