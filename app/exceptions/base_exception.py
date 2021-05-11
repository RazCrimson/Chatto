class ChatApplicationException(BaseException):
    """
    Base exception from with all other applications exceptions will be derived from.
    """
    RESPONSE_CODE = 500
    ERROR_CODE = 0
    MESSAGE = "Application Error"

    @property
    def response_code(self):
        return self.RESPONSE_CODE

    @property
    def error_code(self):
        return self.ERROR_CODE

    def __str__(self):
        return f"<{self.__class__.__name__}: ({self.RESPONSE_CODE}, {self.ERROR_CODE}, {self.MESSAGE}"

    def json(self):
        return {
            "error_code": self.ERROR_CODE,
            "type": self.__class__.__name__,
            "message": self.MESSAGE
        }
