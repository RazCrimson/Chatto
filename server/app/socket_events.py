import time
from datetime import datetime

from flask import request
from flask_jwt_extended import decode_token, exceptions as flask_jwt_exceptions
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, disconnect
from jwt import exceptions as py_jwt_exceptions

from .exceptions import ChatApplicationException, InvalidTokenError
from .models import User, Message

socket_io = SocketIO()


class ChatNamespace(Namespace):
    sid_to_user_id = {}
    user_id_to_sids = {}

    @classmethod
    def on_connect(cls):
        pass

    @classmethod
    def on_jwt(cls, token):
        decoded_token = decode_token(token)
        username = decoded_token['sub']['username']
        user = User.get_user_by_username(username)
        user_id = user.get_id()
        if cls.user_id_to_sids.get(user_id) is None:
            cls.user_id_to_sids[user_id] = set()
        cls.user_id_to_sids[user_id].add(request.sid)
        cls.sid_to_user_id[request.sid] = user_id
        join_room(user_id)
        emit('authenticated')

    @classmethod
    def on_disconnect(cls):
        if cls.sid_to_user_id.get(request.sid) is not None:
            user_id = cls.sid_to_user_id[request.sid]
            leave_room(user_id)
            del cls.sid_to_user_id[request.sid]
            cls.user_id_to_sids[user_id].remove(request.sid)

    @classmethod
    def on_message(cls, json_data):
        sender_id = cls.sid_to_user_id[request.sid]
        receiver_id = json_data['receiver_id']
        message_body = json_data['message_body']
        User.get_user_by_id(receiver_id)
        created_at = datetime.utcnow()
        forwarded_at = None

        if sender_id == receiver_id:
            return

        if cls.user_id_to_sids.get(receiver_id) and len(cls.user_id_to_sids[receiver_id]) != 0:
            forwarded_at = created_at

        msg = Message(sender_id=sender_id,
                      receiver_id=receiver_id,
                      message_body=message_body,
                      created_at=created_at,
                      forwarded_at=forwarded_at)
        msg.save()

        json_data = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message_body": message_body,
            "created_at": str(created_at),
        }
        if forwarded_at:
            emit('message', json_data, to=receiver_id)
        emit('message', json_data, to=sender_id)

    @classmethod
    def on_get_messages(cls, other_user_id):
        user = User.get_user_by_id(cls.sid_to_user_id[request.sid])
        other_user = User.get_user_by_id(other_user_id)
        messages = Message.get_chat_history(user.pk, other_user.pk)
        for m in messages:
            json_data = {
                "sender_id": str(m["sender_id"]),
                "receiver_id": str(m["receiver_id"]),
                "message_body": m["message_body"],
                "created_at": str(m["created_at"]),
            }
            emit('message', json_data)
            time.sleep(0.1)


@socket_io.on_error('/chat')
def error_handler(err):
    if isinstance(err, ChatApplicationException):
        emit('err', err.json())
    elif isinstance(err, py_jwt_exceptions.PyJWTError) or isinstance(err, flask_jwt_exceptions.JWTExtendedException):
        emit('err', InvalidTokenError.json())
    else:
        disconnect()


socket_io.on_namespace(ChatNamespace('/chat'))
