from .base_exception import ChatApplicationException


class AuthException(ChatApplicationException):
    """
    Base Exception for authentication related errors
    """
    RESPONSE_CODE = 403
    ERROR_CODE = 1000
    MESSAGE = "Authentication Error"


class UsernameAlreadyTakenException(AuthException):
    """
    Raised when user requests for a already taken username
    """
    ERROR_CODE = 1001
    MESSAGE = "Username already taken!"


class InvalidPasswordException(AuthException):
    """
    Raised when user sends a wrong password
    """
    ERROR_CODE = 1002
    MESSAGE = "Wrong Password!"


class InvalidTokenException(AuthException):
    """
    Raised when the token is invalid or expired
    """
    ERROR_CODE = 1003
    MESSAGE = "Invalid Token!"
