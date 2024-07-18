from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
from starlette.responses import JSONResponse

from src.auth.utils import Auth
from src.schemas.auth import AuthSchemaWithPhone, AuthSchemaWithEmail
from src.schemas.users import UserByPhone, AuthEmail, AuthEmailWithCode
from src.services.celery import send_email
from src.services.core import User
from src.services.redis import redis_client

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"],
)


@router.post('/phone')
async def auth_phone(user: AuthSchemaWithPhone):
    try:
        await User().add_user(user.identifier, user.platform)
        token = Auth.create_token(user.identifier)
        return JSONResponse(status_code=HTTPStatus.OK, content=token)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка регистрации пользователя по телефону {e}")


@router.post('/email')
async def auth_email(user: AuthSchemaWithEmail):
    try:
        logger.info(f'{user.platform}, {user.identifier}')
        send_email.delay(user.identifier)
        return JSONResponse(status_code=HTTPStatus.OK, content="Код отправлен на почту")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка регистрации пользователя по email {e}")


@router.post('/email/verify')
async def auth_email(user: AuthEmailWithCode):
    try:
        saved_code = redis_client.get(user.email)
        if user.code != saved_code:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"неправильный код")
        else:
            await User().add_user(user.email, "почта")
            token = Auth.create_token(user.email)
            return JSONResponse(status_code=HTTPStatus.OK, content=token)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка после ввода кода по email {e}")
