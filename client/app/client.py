from threading import Lock

import socketio
from requests import Session

from .HTTP_client import HTTPClient
from .crypto import CryptoHandler
from .models import User, Message
from .socketIO_client import SocketIOChatClient

HOST = "http://127.0.0.1:5000"
USER_ENDPOINT = f"{HOST}/user"

sio = socketio.Client()


class Client:

    def __init__(self, username, password, *, do_register=False):
        self.users = {}
        self.session: Session = Session()
        self.http_client: HTTPClient = HTTPClient(self.session)

        if do_register:
            HTTPClient.register(username, password)

        user, crypto_handler = self.http_client.login(username, password)
        self.user: User = user
        self.crypto_handler: CryptoHandler = crypto_handler

        self.screen_buffer: list = []
        self.message_queue: list = []
        self.screen_display_lock: Lock = Lock()
        self.chat_client = SocketIOChatClient('/chat', self.user, self.session, self.message_queue, self.screen_buffer)

        sio.start_background_task(self.message_decryption_loop)
        sio.start_background_task(self.message_display_loop)
        sio.register_namespace(self.chat_client)
        sio.connect(HOST, namespaces=['/chat'], wait_timeout=10, wait=True)

    def message_to_display_text(self, msg: Message):
        try:
            user_id = msg.sender_id
            prefix = 'From '
            if msg.sender_id == self.user.user_id:
                user_id = msg.receiver_id
                prefix = 'To '

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

    def get_user_from_console(self):
        username = input("Username: ")
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
        return user

    @staticmethod
    def print_help():
        print('******** HELP ********\n'
              '0 - this help message\n'
              '1 - toggle auto display of incoming messages(done automatically for 2 and 3).\n'
              '2 - send a message.\n'
              '3 - get user-specific chat history.\n'
              'Any other key to terminate the application.')

    def run_interactive_session(self):
        self.print_help()
        while sio.connected:
            try:
                ch = input()

                if not ch.isdigit():
                    break
                choice = int(ch)
                if choice not in range(4):
                    break
                elif choice == 0:
                    self.print_help()
                elif choice == 1:
                    if self.screen_display_lock.locked():
                        self.screen_display_lock.release()
                    else:
                        self.screen_display_lock.acquire()
                else:
                    if not self.screen_display_lock.locked():
                        self.screen_display_lock.acquire()

                    try:
                        user = self.get_user_from_console()
                        if not user:
                            raise Exception("Not a valid User... :/")

                        if user.user_id == self.user.user_id:
                            raise Exception("U can't speak to yourself :(")

                        if choice == 2:
                            message = input("Message: ")
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
