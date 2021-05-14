from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from ..controllers import UserController
from ..exceptions import ChatApplicationException

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help='username is a required field', required=True)
parser.add_argument('password', type=str, help='password is a required field', required=True)


class UserSignUpResource(Resource):

    def post(self):
        """
        User Account Registration
        """
        data = parser.parse_args()
        username = data.username
        password = data.password
        try:
            return UserController.create(username, password)
        except ChatApplicationException as err:
            return err.json(), err.RESPONSE_CODE


class UserAuthResource(Resource):

    def post(self):
        """
        User Account Authentication
        """
        data = parser.parse_args()
        username = data.username
        password = data.password
        try:
            return UserController.login(username, password)
        except ChatApplicationException as err:
            return err.json(), err.RESPONSE_CODE

    @jwt_required(refresh=True)
    def get(self):
        """
        User Access Token generation
        """
        try:
            return UserController.refresh_access_token()
        except ChatApplicationException as err:
            return err.json(), err.RESPONSE_CODE

    @jwt_required(optional=True, refresh=True)
    def delete(self):
        """
        User Access Token generation
        """
        try:
            return UserController.logout()
        except ChatApplicationException as err:
            return err.json(), err.RESPONSE_CODE
