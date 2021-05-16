from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from ecdsa import ECDH
from ecdsa.curves import NIST521p


class CryptoHandler:
    """
    Class that handles all the cryptography required by the client
    """

    def __init__(self, ecdh=None):
        if ecdh:
            self._ecdh = ecdh
        else:
            self._ecdh = ECDH(NIST521p)
            self._ecdh.generate_private_key()

    def get_public_key(self) -> bytes:
        pub_key = self._ecdh.get_public_key()
        return pub_key.to_pem()

    def get_encrypted_private_key(self, passphrase) -> bytes:
        pem_bytes = self._ecdh.private_key.to_pem()
        return CryptoHandler.AES_encrypt(pem_bytes, passphrase)

    def __str__(self):
        return f"<CryptoHandler: PUBLIC_KEY={self.get_public_key()} >"

    @staticmethod
    def load_from_key(encrypted_key, passphrase):
        pem_bytes = CryptoHandler.AES_decrypt(encrypted_key, passphrase)
        pem_string = pem_bytes.decode('utf-8')
        ecdh = ECDH(NIST521p)
        ecdh.load_private_key_pem(pem_string)
        return CryptoHandler(ecdh)

    @staticmethod
    def SHA256_hash(data: str) -> bytes:
        if type(data) not in [bytes, bytearray]:
            data = str(data).encode('utf-8')
        hash_obj = SHA256.new(data)
        return hash_obj.digest()

    @staticmethod
    def AES_decrypt(encrypted_message, secret) -> bytes:
        session_key = CryptoHandler.SHA256_hash(secret)
        nonce = encrypted_message[:16]
        tag = encrypted_message[16:32]
        ciphertext = encrypted_message[32:]
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return data

    @staticmethod
    def AES_encrypt(data, secret) -> bytes:
        session_key = CryptoHandler.SHA256_hash(secret)
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        encrypted_private_key = b"".join([cipher_aes.nonce, tag, ciphertext])
        return encrypted_private_key

    def encrypt_message_with_key(self, message: str, recipient_pub_pem_bytes) -> bytes:
        message_bytes = message.encode('utf-8')
        recipient_pub_pem = recipient_pub_pem_bytes.decode('utf-8')
        self._ecdh.load_received_public_key_pem(recipient_pub_pem)
        shared_key = self._ecdh.generate_sharedsecret_bytes()
        encrypted_message = CryptoHandler.AES_encrypt(message_bytes, shared_key)
        return encrypted_message

    def decrypt_message(self, encrypted_message: bytes, sender_pub_pem_bytes) -> str:
        sender_pub_pem = sender_pub_pem_bytes.decode('utf-8')
        self._ecdh.load_received_public_key_pem(sender_pub_pem)
        shared_key = self._ecdh.generate_sharedsecret_bytes()
        decrypted_message_bytes = CryptoHandler.AES_decrypt(encrypted_message, shared_key)
        decrypted_message = decrypted_message_bytes.decode('utf-8')
        return decrypted_message


if __name__ == '__main__':
    # Simple test for the module
    msg_text = "Some Random Message"
    d1 = CryptoHandler()
    d2 = CryptoHandler()
    d1_pubkey = d1.get_public_key()
    d2_pubkey = d2.get_public_key()

    d1_privkey = d1.get_encrypted_private_key("Hello")
    d1_clone = CryptoHandler.load_from_key(d1_privkey, "Hello")
    assert d1_clone._ecdh.private_key.to_pem() == d1._ecdh.private_key.to_pem()

    d1._ecdh.load_received_public_key_pem(d2_pubkey.decode('utf-8'))
    d2._ecdh.load_received_public_key_pem(d1_pubkey.decode('utf-8'))
    assert d1._ecdh.generate_sharedsecret() == d2._ecdh.generate_sharedsecret()

    d1_to_d2_message = d1.encrypt_message_with_key(msg_text, d2_pubkey)
    decrypted_text = d2.decrypt_message(d1_to_d2_message, d1_pubkey)
    assert msg_text == decrypted_text

    print("Test Passed")
