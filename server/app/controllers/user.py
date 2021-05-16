from flask import make_response
from flask_jwt_extended import set_refresh_cookies, set_access_cookies, get_jwt_identity, unset_jwt_cookies

from ..authentication import JWTHandler
from ..exceptions import UserNotFoundError, UsernameAlreadyTakenError, InvalidPasswordError
from ..models import User


class UserController:

    @classmethod
    def create(cls, username, password, pub_key, encrypted_priv_key) -> User:
        try:
            User.get_user_by_username(username)
        except UserNotFoundError:
            new_user = User()
            new_user.username = username
            new_user.password = password
            new_user.pub_key = pub_key
            new_user.encrypted_priv_key = encrypted_priv_key
            new_user.save()
            resp = make_response({"msg": f"User: `{new_user.username}` successfully registered!"}, 201)
            return resp
        else:
            raise UsernameAlreadyTakenError

    @classmethod
    def login(cls, username, password):
        user = User.get_user_by_username(username)
        if not user.check_password(password):
            raise InvalidPasswordError

        encrypted_priv_key = user.encrypted_priv_key
        access_token, refresh_token = JWTHandler.generate_tokens(user)
        resp = make_response({
            "msg": f"Logged in!",
            "key": encrypted_priv_key,
            "pub_key": user.pub_key,
            "username": user.username,
            "user_id": user.get_id()
        }, 200)
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp

    @classmethod
    def logout(cls):
        identity = get_jwt_identity()
        msg = "Client is not logged in!"
        if identity:
            msg = f"Logged out in as `{identity['username']}`"
        resp = make_response({"msg": msg}, 200)
        unset_jwt_cookies(resp)
        return resp

    @classmethod
    def refresh_access_token(cls):
        identity = get_jwt_identity()
        access_token = JWTHandler.generate_access_token(identity)
        resp = make_response({"msg": f"Access Token Updated!"}, 200)
        set_access_cookies(resp, access_token)
        return resp

    @classmethod
    def get_details(cls, user_id=None, username=''):
        if user_id:
            user = User.get_user_by_id(user_id)
        else:
            user = User.get_user_by_username(username)
        resp = make_response({
            "msg": f"User Found!",
            "pub_key": user.pub_key,
            "username": user.username,
            "user_id": user.get_id()
        }, 200)
        return resp
