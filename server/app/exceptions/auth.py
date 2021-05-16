from .base_exception import ChatApplicationException


class AuthException(ChatApplicationException):
    """
    Base Exception for authentication related errors
    """
    RESPONSE_CODE = 401
    ERROR_CODE = 1000
    MESSAGE = "Authentication Error"


class UsernameAlreadyTakenError(AuthException):
    """
    Raised when user requests for a already taken username
    """
    ERROR_CODE = 1001
    MESSAGE = "Username already taken!"


class InvalidPasswordError(AuthException):
    """
    Raised when user sends a wrong password
    """
    ERROR_CODE = 1002
    MESSAGE = "Password Mismatch!"


class InvalidTokenError(AuthException):
    """
    Raised when the access token is invalid
    """
    ERROR_CODE = 1100
    MESSAGE = "Invalid or missing Token!"


class InvalidAccessTokenError(InvalidTokenError):
    """
    Raised when the access token is invalid
    """
    ERROR_CODE = 1101
    MESSAGE = "Invalid Access Token!"


class InvalidRefreshTokenError(InvalidTokenError):
    """
    Raised when the refresh token is invalid
    """
    ERROR_CODE = 1102
    MESSAGE = "Invalid Refresh Token!"
