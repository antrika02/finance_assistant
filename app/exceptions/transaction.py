from fastapi import status

from app.exceptions.base import AppException


class TransactionNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = "Transaction not found."


class TransactionAccessDeniedError(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = "You do not have permission to access this transaction."


class InvalidTransactionCategoryError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "The selected category is invalid."
