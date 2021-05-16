class ChatApplicationException(Exception):
    """
    Base exception from with all other applications exceptions will be derived from.
    """
    RESPONSE_CODE = 500
    ERROR_CODE = 0
    MESSAGE = "Application Error"

    @classmethod
    def __str__(cls):
        return f"<{cls.__class__.__name__}: ({cls.RESPONSE_CODE}, {cls.ERROR_CODE}, {cls.MESSAGE}"

    @classmethod
    def json(cls):
        return {
            "error_code": cls.ERROR_CODE,
            "type": str(cls.__name__),
            "msg": cls.MESSAGE
        }
