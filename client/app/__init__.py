from threading import Lock
from typing import Tuple

import socketio
from requests import Session

from .HTTP_client import HTTPClient
from .constants import config
from .crypto import CryptoHandler
from .models import User, Message
from .socketIO_client import SocketIOChatClient

sio = socketio.Client()


class Client:

    def __init__(self, username, password, *, do_register=False):
        self.users = {}
        self.session: Session = Session()
        self.http_client: HTTPClient = HTTPClient(self.session)

        if do_register:
            res, msg = HTTPClient.register(username, password)
            print(msg)

        user, crypto_handler = self.http_client.login(username, password)
        print(f"Logged in as {user.username}")

        self.user: User = user
        self.prev_user = None # To default to previous user (to reduce typing)
        self.crypto_handler: CryptoHandler = crypto_handler

        self.screen_buffer: list = []
        self.message_queue: list = []
        self.screen_display_lock: Lock = Lock()
        self.chat_client = SocketIOChatClient('/chat', self.user, self.http_client, self.message_queue,
                                              self.screen_buffer)

        sio.register_namespace(self.chat_client)

        print('Establishing a SocketIO connection to the server...')
        print('The server on Heroku is running on gunicorn which is not the best with socketIO. '
              'So retry in case the socketIO connection fails :)')
        sio.connect(config['HOST'], namespaces=['/chat'], wait_timeout=30, wait=True)
        sio.start_background_task(self.message_decryption_loop)
        sio.start_background_task(self.message_display_loop)

    def message_to_display_text(self, msg: Message):
        try:
            user_id = msg.sender_id
            prefix = 'From'
            if msg.sender_id == self.user.user_id:
                user_id = msg.receiver_id
                prefix = ' To '

            user = self.users.get(user_id)
            if user is None:
                user = self.http_client.get_user_details(user_id=user_id)
                if not user:
                    return
                self.users[user_id] = user

            msg_string = self.crypto_handler.decrypt_message(msg.message_body, user.public_key)

            return f"{prefix} `{user.username}` at {msg.created_at.strftime('%H:%M:%S, %d %B %Y')} : {msg_string}"
        except Exception as e:
            print("Message Decrypter : ", e)

    def message_decryption_loop(self):
        while sio.connected:
            try:
                if len(self.message_queue) == 0:
                    sio.sleep(0.5)
                    continue
                data = self.message_queue.pop(0)

                if isinstance(data, Message):
                    data = self.message_to_display_text(data)

                if not data:
                    continue
                self.screen_buffer.append(data)
            except:
                pass

    def message_display_loop(self):
        while sio.connected:
            if len(self.screen_buffer) != 0:
                msg = self.screen_buffer.pop(0)
            else:
                msg = None

            if msg is None:
                sio.sleep(0.3)
                continue
            self.screen_display_lock.acquire()
            try:
                print(msg)
            except Exception as e:
                print("Message Presenter: ", e)
            self.screen_display_lock.release()

    def get_user_from_string(self, username):
        if username == '':
            return self.prev_user
        user = None
        for _id, user_obj in self.users.items():
            if username == user_obj.username:
                user = user_obj
                break
        if not user:
            user = self.http_client.get_user_details(username=username)
            if not user:
                return
            self.users[user.user_id] = user
        self.prev_user = user
        return user

    @staticmethod
    def parse_user_and_message_body(string: str) -> Tuple[str, str]:
        user_msg_split = string.find('/')
        if user_msg_split == 0:
            return '', string[1:]
        elif user_msg_split == -1:
            return '', string
        elif user_msg_split == len(string):
            return string[:user_msg_split], ''
        return string[:user_msg_split], string[user_msg_split + 1:]

    @staticmethod
    def print_help():
        print('\n******** HELP ********\n'
              '0 - this help message\n'
              '1 - toggle auto display of incoming messages(done automatically for 2 and 3).\n'
              '`<username>/<message>` -  to send a message.\n'
              '`<username>/` - get user-specific chat history.\n'
              'Press Ctrl + C to terminate the application.\n')

    def run_interactive_session(self):
        self.print_help()
        while sio.connected:
            try:
                choice = input()

                if choice == '0':
                    self.print_help()
                elif choice == '1':
                    if self.screen_display_lock.locked():
                        self.screen_display_lock.release()
                    else:
                        self.screen_display_lock.acquire()
                else:
                    if not self.screen_display_lock.locked():
                        self.screen_display_lock.acquire()

                    try:
                        user_string, message = self.parse_user_and_message_body(choice)
                        user = self.get_user_from_string(user_string)
                        if not user:
                            raise Exception("Not a valid User... :/")

                        if user.user_id == self.user.user_id:
                            raise Exception("U can't speak to yourself :(")

                        if message != '':
                            msg_body = self.crypto_handler.encrypt_message_with_key(message, user.public_key)
                            self.chat_client.send_message(user.user_id, msg_body)
                        else:
                            self.chat_client.get_messages(user.user_id)
                    except Exception as err:
                        print(err)
                    self.screen_display_lock.release()
            except KeyboardInterrupt:
                break
        print('Exiting Application...')
        if sio.connected:
            sio.disconnect()
        sio.wait()
