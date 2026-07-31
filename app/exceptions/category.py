from app.exceptions.base import AppException


class CategoryNotFoundError(AppException):
    status_code = 404

    def __init__(self):
        super().__init__("Category not found.")


class CategoryAccessDeniedError(AppException):
    status_code = 403

    def __init__(self):
        super().__init__("You do not have permission to access this category.")