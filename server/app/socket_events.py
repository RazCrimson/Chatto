from bidict import bidict
from flask import request
from flask_jwt_extended import decode_token
from flask_socketio import SocketIO, Namespace, ConnectionRefusedError,  emit, join_room

from .models import User

socket_io = SocketIO(cors_allowed_origins="*")


class ChatNamespace(Namespace):
    current_connections = bidict()

    @classmethod
    def on_connect(cls):
        emit('jwt')

    @classmethod
    def on_jwt(cls, token):
        decoded_token = decode_token(token)
        username = decoded_token['sub']['username']
        user = User.get_user_by_username(username)
        mongo_id = user.get_mongo_id()
        if cls.current_connections.get(mongo_id) is not None:
            raise Exception
        cls.current_connections[mongo_id] = request.sid

    @classmethod
    def on_disconnect(cls):
        if cls.current_connections.inverse.get(request.sid) is not None:
            del cls.current_connections.inverse[request.sid]

    @classmethod
    def on_message(cls, message_dict):
        pass


socket_io.on_namespace(ChatNamespace('/chat'))
