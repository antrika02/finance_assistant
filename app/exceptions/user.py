from fastapi import status

from app.exceptions.base import AppException


class UserAlreadyExistsError(AppException):
    status_code = status.HTTP_409_CONFLICT
    default_message = "User already exists."


class UserNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = "User not found."


class InvalidCredentialsError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = "Invalid email or password."