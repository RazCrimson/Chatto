from datetime import datetime

from bidict import bidict
from flask import request
from flask_jwt_extended import decode_token
from flask_socketio import SocketIO, Namespace, emit, disconnect

from .exceptions import ChatApplicationException
from .models import User, Message

socket_io = SocketIO()


def custom_error_handler(err_event="err"):
    """
     A custom parameterised decorator to handle exceptions for socketIO interactions
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except ChatApplicationException as err:
                emit(err_event, err.MESSAGE)
            except Exception as err:
                print('Disconnecting with client due to error: ', type(err), err)
                emit(err_event, {})
                disconnect()

        return wrapper

    return decorator


class ChatNamespace(Namespace):
    current_connections = bidict()

    @classmethod
    def on_connect(cls):
        pass

    @classmethod
    def on_jwt(cls, token):
        decoded_token = decode_token(token)
        username = decoded_token['sub']['username']
        user = User.get_user_by_username(username)
        user_id = user.get_id()
        if cls.current_connections.get(user_id) is not None:
            raise ChatApplicationException('Only one client is allowed for a user')
        cls.current_connections[user_id] = request.sid

        message = Message.get_unreceived_messages(user_id)
        emit('authenticated', message)

    @classmethod
    def on_disconnect(cls):
        if cls.current_connections.inverse.get(request.sid) is not None:
            del cls.current_connections.inverse[request.sid]

    @classmethod
    def on_message(cls, json_data):
        receiver_id = json_data['receiver_id']
        message_body = json_data['message_body']
        User.get_user_by_id(receiver_id)
        sender_id = cls.current_connections.inverse[request.sid]
        created_at = datetime.utcnow()
        forwarded_at = None

        if sender_id == receiver_id:
            return

        receiver_sid = cls.current_connections.get(receiver_id)
        if receiver_sid:
            forwarded_at = created_at

        msg = Message(sender_id=sender_id,
                      receiver_id=receiver_id,
                      message_body=message_body,
                      created_at=created_at,
                      forwarded_at=forwarded_at)
        msg.save()
        if forwarded_at:
            json_data = {
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "message_body": message_body,
                "created_at": str(created_at),
            }
            emit('message', json_data)
            emit('message', json_data, to=receiver_sid)

    @classmethod
    def on_get_messages(cls, other_user_id):
        other_user = User.get_user_by_id(other_user_id)
        user = User.get_user_by_id(cls.current_connections.inverse[request.sid])
        messages = Message.get_chat_history(user.pk, other_user.pk)
        json_data = [
            {
                "sender_id": str(m["sender_id"]),
                "receiver_id": str(m["receiver_id"]),
                "message_body": m["message_body"],
                "created_at": str(m["created_at"]),
            }
            for m in messages]
        emit('messages', json_data)

    @classmethod
    def on_list_of_connections(cls):
        user_id = cls.current_connections.get(request.sid)
        if not user_id:
            raise ChatApplicationException('User not Authenticated')


socket_io.on_namespace(ChatNamespace('/chat'))
