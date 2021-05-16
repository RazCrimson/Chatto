from datetime import datetime

from bidict import bidict
from flask import request
from flask_jwt_extended import decode_token
from flask_socketio import SocketIO, Namespace, emit, disconnect, join_room, leave_room

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
    sid_to_user_id = {}
    user_id_to_sids = {}
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
        if cls.user_id_to_sids.get(user_id) is None:
            cls.user_id_to_sids[user_id] = set()
        cls.user_id_to_sids[user_id].add(request.sid)
        cls.sid_to_user_id[request.sid] = user_id
        # cls.current_connections[user_id] = request.sid
        join_room(user_id)
        # message = Message.get_unreceived_messages(user_id)
        emit('authenticated', {})

    @classmethod
    def on_disconnect(cls):
        if cls.sid_to_user_id.get(request.sid) is not None:
            user_id = cls.sid_to_user_id[request.sid]
            leave_room(user_id)
            del cls.sid_to_user_id[request.sid]
            cls.user_id_to_sids[user_id].remove(request.sid)

    @classmethod
    def on_message(cls, json_data):
        receiver_id = json_data['receiver_id']
        message_body = json_data['message_body']
        User.get_user_by_id(receiver_id)
        sender_id = cls.sid_to_user_id[request.sid]
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
        emit('messages', messages)

    @classmethod
    def on_list_of_connections(cls):
        user_id = cls.current_connections.get(request.sid)
        if not user_id:
            raise ChatApplicationException('User not Authenticated')


socket_io.on_namespace(ChatNamespace('/chat'))
