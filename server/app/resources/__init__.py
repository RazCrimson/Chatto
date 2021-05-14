from flask_restful import Api

from .user import UserAuthResource, UserSignUpResource

api = Api()

api.add_resource(UserSignUpResource, '/register')
api.add_resource(UserAuthResource, '/user')
