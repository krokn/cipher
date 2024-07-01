import base64
import hashlib

from loguru import logger

from config import SECRET_FOR_TOKEN


def encoded_base64(string):
    encoded_bytes = base64.b64encode(string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")
    return encoded_string


def decode_base64(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode("utf-8")
    return decoded_string


def hashed_string(str):
    str_bytes = str.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(str_bytes)
    hashed_str = sha256.hexdigest()
    return hashed_str


def create_token(phone: str):
    encoded_phone = encoded_base64(phone)
    token = encoded_phone + "||" + hashed_string(encoded_phone + SECRET_FOR_TOKEN)
    logger.info(f'token={token}')
    return token
