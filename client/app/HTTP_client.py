import json
from base64 import b64encode, b64decode
from typing import Tuple, Union

import requests

from .constants import config
from .crypto import CryptoHandler
from .models import User


class HTTPClient:
    def __init__(self, session: requests.Session):
        self.session = session
        self.is_authenticated = False

    @staticmethod
    def register(username, password) -> Tuple[bool, str]:
        # Generate Keys
        crypto_handler = CryptoHandler()
        public_key = b64encode(crypto_handler.get_public_key())
        encrypted_priv_key = b64encode(crypto_handler.get_encrypted_private_key(passphrase=password))
        hashed_password = b64encode(CryptoHandler.SHA256_hash(password))

        # Format Request Body
        data = {
            "username": username,
            "password": hashed_password.decode(),
            "pub_key": public_key.decode(),
            "encrypted_priv_key": encrypted_priv_key.decode()
        }

        # Parse Response
        resp = requests.post(config['HOST'] + '/user/register', json=data)
        response_json = json.loads(resp.text)
        msg = response_json['msg']

        if resp.status_code == 201:
            return True, msg
        return False, msg

    def login(self, username, password) -> Tuple[User, CryptoHandler]:
        # Format Request Body
        hashed_password = b64encode(CryptoHandler.SHA256_hash(password))
        data = {
            "username": username,
            "password": hashed_password.decode()
        }

        res = self.session.post(config['HOST'] + '/user/signin', json=data)
        if res.status_code != 200:
            raise Exception('Invalid Credentials')
        response_json = json.loads(res.text)

        # Parse Response for user details and Keys
        username = response_json['username']
        user_id = response_json['user_id']
        pub_key = b64decode(response_json['pub_key'])
        encoded_priv_key = response_json['key']
        decoded_priv_key = b64decode(encoded_priv_key)

        # Generating User object and loading crypto handler with private key
        user = User(user_id, username, pub_key)
        crypto_handler = CryptoHandler.load_from_key(decoded_priv_key, passphrase=password)

        return user, crypto_handler

    def refresh_access_token(self) -> bool:
        res = self.session.get(config['HOST'] + '/user/refresh')
        if res.status_code == 200:
            return True
        self.is_authenticated = False
        return False

    def get_user_details(self, user_id=None, username='', retry=1) -> Union[User, bool]:
        query = '?'
        if user_id:
            query += f'user_id={user_id}'
        else:
            query += f'username={username}'

        res = self.session.get(config['HOST'] + '/user/details' + query)
        if res.status_code != 200:
            if retry:
                self.refresh_access_token()
                return self.get_user_details(user_id, username, 0)
            return False

        response_json = json.loads(res.text)
        username = response_json['username']
        user_id = response_json['user_id']
        pub_key = b64decode(response_json['pub_key'])
        user = User(user_id, username, pub_key)
        return user

    def logout(self):
        res = self.session.delete(config['HOST'] + '/user/signout')
        response_json = json.loads(res.text)
        print(response_json.get('msg'))
