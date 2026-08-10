from app.exceptions.base import AppException


class AIServiceException(AppException):
    """
    Raised when the AI service cannot process a request.
    """

    status_code = 503
    default_message = "AI service is temporarily unavailable."
