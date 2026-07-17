"""PyForTG custom exceptions."""


class PyForTGException(Exception):
    """Base exception for PyForTG."""
    pass


class APIException(PyForTGException):
    """Exception raised for Telegram API errors."""
    
    def __init__(
        self,
        error_code: int,
        description: str,
        response: dict = None,
    ):
        self.error_code = error_code
        self.description = description
        self.response = response or {}
        super().__init__(f"API Error {error_code}: {description}")


class ValidationException(PyForTGException):
    """Exception raised for validation errors."""
    pass


class ConnectionException(PyForTGException):
    """Exception raised for connection errors."""
    pass


class TimeoutException(PyForTGException):
    """Exception raised for request timeouts."""
    pass


class FileNotFoundException(PyForTGException):
    """Exception raised when a file cannot be found."""
    pass


class HandlerException(PyForTGException):
    """Exception raised in handler execution."""
    pass


class MiddlewareException(PyForTGException):
    """Exception raised in middleware execution."""
    pass


class StorageException(PyForTGException):
    """Exception raised for storage operations."""
    pass


class WebhookException(PyForTGException):
    """Exception raised for webhook-related errors."""
    pass
