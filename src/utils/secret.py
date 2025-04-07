from cryptography.fernet import Fernet

from src.config import config


def encode_secret(secret: str) -> str:
    cipher_suite = Fernet(config.app.encryption_key)
    encoded_secret: str = cipher_suite.encrypt(secret.encode())
    return encoded_secret


def decode_secret(encoded_secret: str) -> str:
    cipher_suite = Fernet(config.app.encryption_key)
    secret = cipher_suite.decrypt(encoded_secret)
    return secret.decode()
