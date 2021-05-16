from datetime import datetime
from typing import Union


class User:
    def __init__(self, user_id: str, username: str, public_key):
        self.user_id: str = user_id
        self.username: str = username
        self.public_key = public_key


class Message:
    def __init__(self, sender_id: str, receiver_id: str, message_body: bytes, created_at: Union[str, datetime]):
        self.sender_id: str = sender_id
        self.receiver_id: str = receiver_id
        self.message_body: bytes = message_body
        if type(created_at) is datetime:
            self.created_at: datetime = created_at
        else:
            self.created_at: datetime = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f")
