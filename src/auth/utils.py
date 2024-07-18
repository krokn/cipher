import base64
import hashlib

from loguru import logger

from config import SECRET_FOR_TOKEN
from src.services.encryption import Encrypt


class Auth:
    @staticmethod
    def create_token(identifier: str):
        encoded_identification_string = Encrypt.encoded(identifier)
        token = encoded_identification_string + "||" + Encrypt.hashed(encoded_identification_string + SECRET_FOR_TOKEN)
        logger.info(f'token={token}')
        return token

