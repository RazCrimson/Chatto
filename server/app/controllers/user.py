from flask import make_response
from flask_jwt_extended import set_refresh_cookies, set_access_cookies, get_jwt_identity, unset_jwt_cookies

from ..authentication import JWTHandler
from ..exceptions import UserNotFoundError, UsernameAlreadyTakenError, InvalidPasswordError
from ..models import User


class UserController:

    @classmethod
    def create(cls, username, password) -> User:
        try:
            User.get_user_by_username(username)
        except UserNotFoundError:
            new_user = User()
            new_user.username = username
            new_user.password = password
            new_user.save()
            resp = make_response({"message": f"User: `{new_user.username}` successfully registered!"}, 201)
            return resp
        else:
            raise UsernameAlreadyTakenError

    @classmethod
    def login(cls, username, password):
        user = User.get_user_by_username(username)
        if not user.check_password(password):
            raise InvalidPasswordError

        access_token, refresh_token = JWTHandler.generate_tokens(user)
        resp = make_response({"message": f"Logged in as `{user.username}`"}, 200)
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp

    @classmethod
    def logout(cls):
        identity = get_jwt_identity()
        msg = "Client was never logged in!"
        if identity:
            msg = f"Logged out in as `{identity['username']}`"
        resp = make_response({"message": msg}, 200)
        unset_jwt_cookies(resp)
        return resp

    @classmethod
    def refresh_access_token(cls):
        identity = get_jwt_identity()
        access_token = JWTHandler.generate_access_token(identity)
        resp = make_response({"message": f"Access Token Updated!"}, 200)
        set_access_cookies(resp, access_token)
        return resp
