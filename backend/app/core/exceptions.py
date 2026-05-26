class AppException(Exception):
    """Base exception for the application."""

    pass


class UserNotFoundError(AppException):
    """Raised when a user cannot be found."""

    pass


class UserAlreadyExistsError(AppException):
    """Raised when attempting to create a user that already exists."""

    pass


class UnauthorizedAction(AppException):
    """Raised when attempting to perform an unauthorized action."""

    pass
