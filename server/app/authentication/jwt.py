from flask import make_response
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, unset_jwt_cookies, jwt_required, \
    unset_access_cookies

from ..exceptions import InvalidTokenError, InvalidAccessTokenError
from ..models import User

jwt = JWTManager()


class JWTHandler:

    @classmethod
    def generate_tokens(cls, user: User):
        session_data = {"id": user.get_id(), "username": user.username}
        access_token = create_access_token(identity=session_data, fresh=True)
        refresh_token = create_refresh_token(identity=session_data)
        return access_token, refresh_token

    @classmethod
    def generate_access_token(cls, identity):
        return create_access_token(identity=identity, fresh=False)

    @staticmethod
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        resp = make_response(InvalidAccessTokenException().json(), InvalidAccessTokenException.RESPONSE_CODE)
        return resp

    @staticmethod
    @jwt.expired_token_loader
    def expired_token_callback(callback):
        resp = make_response(InvalidAccessTokenException().json(), InvalidAccessTokenException.RESPONSE_CODE)
        unset_access_cookies(resp)
        return resp

    @staticmethod
    @jwt.expired_token_loader
    def expired_token_callback(callback):
        resp = make_response(InvalidAccessTokenException().json(), InvalidAccessTokenException.RESPONSE_CODE)
        unset_access_cookies(resp)
        return resp

    @staticmethod

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        resp = make_response(InvalidTokenException().json(), InvalidTokenException.RESPONSE_CODE)
        unset_jwt_cookies(resp)
        return resp

