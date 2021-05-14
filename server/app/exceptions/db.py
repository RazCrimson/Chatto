from .base_exception import ChatApplicationException


class DatabaseException(ChatApplicationException):
    """
    Base Exception for database related errors
    """
    ERROR_CODE = 2000
    MESSAGE = "Database Error"


class NotFoundException(DatabaseException):
    """
    Raised when a resource can't be found in the database
    """
    RESPONSE_CODE = 404
    ERROR_CODE = 2100
    MESSAGE = "Resource not found!"


class UserNotFoundException(NotFoundException):
    """
    Raised when a resource can't be found in the database
    """
    ERROR_CODE = 2101
    MESSAGE = "User not found!"
