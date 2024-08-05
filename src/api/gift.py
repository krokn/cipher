from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Header
from src.logging.logger import logger
from starlette.responses import JSONResponse

from src.services.core import User
from src.services.encryption import Encrypt

router = APIRouter(
    prefix="/api/gift",
    tags=["Gift"],
)


@router.post('/subscribe/refresh')
async def refresh_subscribe(token: str | None = Header(default=None)):
    try:
        identifier = token
        if '||' in token:
            identifier = Encrypt.get_user_by_token(token)
        await User().refresh_subscription_user(identifier)
        return JSONResponse(status_code=HTTPStatus.OK, content='subscribe refresh success')
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f'error refresh subscribe = {str(e)}, identifier = {identifier}')
        raise HTTPException(status_code=500, detail=str(e))


@router.patch('/subscribe')
async def change_subscribe(token: str | None = Header(default=None), type_subscribe: str = 'обычная-подписка'):
    try:
        identifier = token
        if '||' in token:
            identifier = Encrypt.get_user_by_token(token)
        await User().change_subscribe_user(identifier, type_subscribe)
        return JSONResponse(status_code=HTTPStatus.OK, content='Подписка изменена')
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f'error change subscribe = {str(e)}, identifier = {identifier}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('')
async def add_gift(token: str | None = Header(default=None), name_gift: str = 'обычная-подписка'):
    try:
        identifier = token
        if '||' in token:
            identifier = Encrypt.get_user_by_token(token)
        await User().add_gift_user(identifier, name_gift)
        return JSONResponse(status_code=HTTPStatus.OK, content='Подарок успешно добавлен')
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f'error add gift = {str(e)}, identifier = {identifier}')
        raise HTTPException(status_code=500, detail=str(e))

