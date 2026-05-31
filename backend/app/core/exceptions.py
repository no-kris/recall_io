class AppException(Exception):
    """Base exception for the application."""

    pass


class UserNotFoundError(AppException):
    """Raised when a user cannot be found."""

    pass


class NoteNotFoundError(AppException):
    """Raised when a note object cannot be found."""

    pass


class UserAlreadyExistsError(AppException):
    """Raised when attempting to create a user that already exists."""

    pass


class MissingNeededValuesError(AppException):
    """Raised when needed values are missing."""

    pass
