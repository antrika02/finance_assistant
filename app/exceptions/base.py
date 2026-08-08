class AppException(Exception):
    """
    Base exception for all application exceptions.
    """

    status_code = 400
    default_message = "Application error."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)
