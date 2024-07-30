from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from loguru import logger
from starlette.responses import JSONResponse

from src.auth.utils import Auth
from src.repositories.users import UserRepository
from src.schemas.auth import AuthSchemaWithPhone, AuthSchemaWithEmail
from src.schemas.users import AuthEmailWithCode
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
        if await UserRepository().get_user_by_identifier(user.identifier) is not None:
            raise HTTPException(status_code=403, detail=f"пользователь уже существует")
        await User().add_user(user.identifier, user.platform)
        token = Auth.create_token(user.identifier)
        return JSONResponse(status_code=HTTPStatus.OK, content=token)
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)


@router.post('/phone/login')
async def auth_phone(user: AuthSchemaWithPhone):
    try:
        if await UserRepository().get_user_by_identifier(user.identifier) is None:
            raise HTTPException(status_code=404, detail=f"пользователь не существует")
        token = Auth.create_token(user.identifier)
        return JSONResponse(status_code=HTTPStatus.OK, content=token)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})


@router.post('/email')
async def auth_email(user: AuthSchemaWithEmail):
    try:
        logger.info(f'{user.platform}, {user.identifier}')
        if await UserRepository().get_user_by_identifier(user.identifier) is not None:
            raise HTTPException(status_code=403, detail=f"пользователь уже существует")
        send_email.delay(user.identifier)
        return JSONResponse(status_code=HTTPStatus.OK, content="Код отправлен на почту")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post('/email/login')
async def auth_email(user: AuthSchemaWithEmail):
    try:
        logger.info(f'{user.platform}, {user.identifier}')
        send_email.delay(user.identifier)
        return JSONResponse(status_code=HTTPStatus.OK, content="Код отправлен на почту")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post('/email/verify')
async def auth_email(user: AuthEmailWithCode):
    try:
        saved_code = redis_client.get(user.email)
        if user.code != saved_code:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"неправильный код")
        else:
            if await UserRepository().get_user_by_identifier(user.email) is None:
                await User().add_user(user.email, "почта")
            token = Auth.create_token(user.email)
            return JSONResponse(status_code=HTTPStatus.OK, content=token)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
