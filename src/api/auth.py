from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from loguru import logger
from starlette.responses import JSONResponse

from src.auth.utils import Auth
from src.schemas.users import UserByPhone, AuthEmail, AuthEmailWithCode
from src.services.celery import send_email
from src.services.core import User
from src.services.redis import redis_client

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"],
)


@router.post('/phone')
async def auth_phone(user: UserByPhone):
    try:
        await User().add_user(user)
        token = Auth.create_token(user.phone)
        return JSONResponse(status_code=HTTPStatus.OK, content=token)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка регистрации пользователя по телефону {e}")


@router.post('/email')
async def auth_email(user: AuthEmail):
    try:
        send_email.delay(user.email)
        return JSONResponse(status_code=HTTPStatus.OK, content="Код отправлен на почту")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка регистрации пользователя по email {e}")


@router.post('/email/verify')
async def auth_email(user: AuthEmailWithCode):
    try:
        email = user.email
        user_code = user.code
        logger.info(f'email = {email}')
        logger.info(f'user_code = {user_code}')
        saved_code = redis_client.get(email)
        logger.info(f'saved_code = {saved_code}')
        if user_code != saved_code:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"не правильный код")
        else:
            user = UserByPhone(phone=email)
            await User().add_user(user)
            token = Auth.create_token(email)
            return JSONResponse(status_code=HTTPStatus.OK, content=token)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка после ввода кода по email {e}")
