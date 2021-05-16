from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token

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
