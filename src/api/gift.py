from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from loguru import logger
from starlette.responses import JSONResponse

from src.services.core import User
from src.services.encryption import Encrypt

router = APIRouter(
    prefix="/api/gift",
    tags=["Gift"],
)


@router.post('/subscribe/refresh')
async def refresh_subscribe(token_or_phone: str):
    try:
        identifier = token_or_phone
        if '||' in token_or_phone:
            identifier = Encrypt.get_user_by_token(token_or_phone)
        await User().refresh_subscription_user(identifier)
        return JSONResponse(status_code=HTTPStatus.OK, content='Подписка обновлена')
    except Exception as e:
        logger.info(f'ошибка при обновлении подписки = {e}, телефон = {identifier}')
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка добавления подписки пользователю {e}")


@router.patch('/subscribe')
async def change_subscribe(token_or_phone: str, type_subscribe: str = 'обычная-подписка'):
    try:
        identifier = token_or_phone
        if '||' in token_or_phone:
            identifier = Encrypt.get_user_by_token(token_or_phone)
        await User().change_subscribe_user(identifier, type_subscribe)
        return JSONResponse(status_code=HTTPStatus.OK, content='Подписка изменена')
    except Exception as e:
        logger.info(f'ошибка при обновлении подписки = {e}, телефон = {identifier}')
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка добавления подписки пользователю {e}")


@router.post('')
async def add_gift(token_or_phone: str, name_gift: str):
    try:
        identifier = token_or_phone
        if '||' in token_or_phone:
            identifier = Encrypt.get_user_by_token(token_or_phone)
        await User().add_gift_user(identifier, name_gift)
        return JSONResponse(status_code=HTTPStatus.OK, content='Подарок успешно добавлен')
    except Exception as e:
        logger.info(f'ошибка при добавлении подарка пользователю = {e}, индетификация = {identifier}')
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка добавления сердец пользователю {e}")

