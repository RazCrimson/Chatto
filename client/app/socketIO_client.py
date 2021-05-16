from socketio import ClientNamespace

from .HTTP_client import HTTPClient
from .constants import config
from .models import User, Message


class SocketIOChatClient(ClientNamespace):

    def __init__(self, namespace, user: User, http_client: HTTPClient, shared_message_queue: list, shared_buffer: list):
        self.user = user
        self.http_client = http_client
        self.shared_message_queue = shared_message_queue
        self.shared_buffer = shared_buffer
        self.is_authenticated = False
        super().__init__(namespace=namespace)

    def on_connect(self):
        print(f"Connected to server.\nAuthenticating as {self.user.username}...")
        cookies = self.http_client.session.cookies._cookies[config['DOMAIN']]
        cookie = cookies['/']['access_token_cookie']
        token = cookie.value
        self.emit('jwt', token)

    def on_disconnect(self):
        print('Disconnected from server....')

    def on_err(self, err_json):
        if err_json.get('status_code') == 401:
            self.is_authenticated = False
            self.http_client.refresh_access_token()
        else:
            print('Error from Server:', err_json.get('msg'))

    def on_authenticated(self):
        self.is_authenticated = True
        print('Authentication Succeeded!')

    def on_message(self, json_data):
        sender_id = json_data.get('sender_id')
        receiver_id = json_data.get('receiver_id')
        message_body = json_data.get('message_body')
        created_at = json_data.get('created_at')

        if sender_id and receiver_id and message_body and created_at:
            msg = Message(sender_id, receiver_id, message_body, created_at)
            self.shared_message_queue.append(msg)

    def send_message(self, receiver_id, message_body):
        json_data = {
            "receiver_id": receiver_id,
            "message_body": message_body
        }
        self.emit('message', json_data)

    def get_messages(self, receiver_id):
        self.emit('get_messages', receiver_id)
