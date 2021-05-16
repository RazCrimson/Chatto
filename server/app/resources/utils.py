from flask import make_response
from flask_restful import Api
from jwt import exceptions as py_jwt_exceptions
from flask_jwt_extended import unset_jwt_cookies, exceptions as flask_jwt_exceptions
from ..exceptions import ChatApplicationException, InvalidTokenError


class ExtendedAPI(Api):
    """
     A custom API class to handle errors
    """

    def handle_error(self, e):
        if isinstance(e, ChatApplicationException):
            return e.json(), e.RESPONSE_CODE
        elif isinstance(e, py_jwt_exceptions.PyJWTError) or isinstance(e, flask_jwt_exceptions.JWTExtendedException):
            resp = make_response(InvalidTokenError.json(), InvalidTokenError.RESPONSE_CODE)
            unset_jwt_cookies(resp)
            return resp
        return ChatApplicationException.json(), ChatApplicationException.RESPONSE_CODE
