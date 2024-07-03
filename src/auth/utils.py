import base64
import hashlib

from loguru import logger

from config import SECRET_FOR_TOKEN
from src.services.encryption import Encrypt


class Auth:
    @staticmethod
    def create_token(phone: str):
        encoded_phone = Encrypt.encoded(phone)
        token = encoded_phone + "||" + Encrypt.hashed(encoded_phone + SECRET_FOR_TOKEN)
        logger.info(f'token={token}')
        return token
