from fastapi import status

from app.exceptions.base import AppException


class UserAlreadyExistsError(AppException):
    status_code = status.HTTP_409_CONFLICT


class UserNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND

class InvalidCredentialsError(AppException):
    status_code = 401

    def __init__(self):
        super().__init__("Invalid email or password.")