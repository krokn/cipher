import base64
import hashlib

from loguru import logger

from config import SECRET_FOR_TOKEN


class Encrypt:

    @staticmethod
    def encoded(string):
        encoded_bytes = base64.b64encode(string.encode("utf-8"))
        encoded_string = encoded_bytes.decode("utf-8")
        return encoded_string

    @staticmethod
    def decoded(encoded_string):
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode("utf-8")
        return decoded_string

    @staticmethod
    def hashed(str):
        str_bytes = str.encode('utf-8')
        sha256 = hashlib.sha256()
        sha256.update(str_bytes)
        hashed_str = sha256.hexdigest()
        return hashed_str

    @staticmethod
    def get_phone_by_token(token: str):
        try:
            encoded_phone = token.split("||")[0]
            user_signatura = token.split("||")[1]
            phone = Encrypt.decoded(encoded_phone)
            token_server = Encrypt.create_token(phone)
            server_signatura = token_server.split("||")[1]
            logger.info(f'server_signatura = {server_signatura}')
            logger.info(f'user_signatura = {user_signatura}')
            if user_signatura == server_signatura:
                return phone
        except:
            return None

    @staticmethod
    def create_token(phone: str):
        encoded_phone = Encrypt.encoded(phone)
        token = encoded_phone + "||" + Encrypt.hashed(encoded_phone + SECRET_FOR_TOKEN)
        logger.info(f'token={token}')
        return token