from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from ..controllers import UserController
from ..exceptions import AuthException

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help='username is custom_private_key required field', required=True)
parser.add_argument('password', type=str, help='password is custom_private_key required field', required=True)
parser.add_argument('pub_key', type=str, help='pub_key is custom_private_key required field')
parser.add_argument('encrypted_priv_key', type=str, help='encrypted_priv_key is custom_private_key required field')


class UserSignUpResource(Resource):

    def post(self):
        """
        User Account Registration
        """
        data = parser.parse_args()
        # TODO: Add more validations here
        username = data.username
        password = data.password
        if not data.pub_key or not data.encrypted_priv_key:
            raise AuthException
        pub_key = data.pub_key
        encrypted_priv_key = data.encrypted_priv_key
        return UserController.register(username, password, pub_key, encrypted_priv_key)


class UserSignInResource(Resource):

    def post(self):
        """
        User Account Authentication
        """
        data = parser.parse_args()
        username = data.username
        password = data.password
        return UserController.login(username, password)


class UserRefreshResource(Resource):

    @jwt_required(refresh=True)
    def get(self):
        """
        User Access Token generation
        """
        return UserController.refresh_access_token()


class UserSignOutResource(Resource):

    @jwt_required(optional=True, refresh=True)
    def delete(self):
        """
        User Logout
        """
        return UserController.logout()


class UserDetailsResource(Resource):

    @jwt_required()
    def get(self):
        """
        Get Public User information
        """

        query = request.args
        user_id = query.get('user_id')
        username = query.get('username')
        if user_id:
            return UserController.get_details(user_id=user_id)
        return UserController.get_details(username=username)

