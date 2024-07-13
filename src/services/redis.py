import random

import redis

redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)


def create_code_for_email_and_save_code(email: str):
    code = create_code()
    redis_client.set(email, code, ex=600)
    return code


def create_code():
    return random.randint(1000, 9999)