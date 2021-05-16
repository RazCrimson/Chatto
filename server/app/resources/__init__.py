from .utils import ExtendedAPI

from .user import UserSignInResource, UserSignUpResource, UserDetailsResource, UserRefreshResource, UserSignOutResource

api = ExtendedAPI()

api.add_resource(UserSignUpResource, '/user/register')
api.add_resource(UserSignInResource, '/user/signin')
api.add_resource(UserSignOutResource, '/user/signout')
api.add_resource(UserRefreshResource, '/user/refresh')
api.add_resource(UserDetailsResource, '/user/details')
