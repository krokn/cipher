from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Header
from loguru import logger
from starlette.responses import JSONResponse

from src.repositories.users import UserRepository
from src.services.core import User
from src.services.encryption import Encrypt

router = APIRouter(
    prefix="/api/user",
    tags=["Users"],
)


@router.get('')
async def get_user(token: str | None = Header(default=None)):
    try:
        identifier = Encrypt.get_user_by_token(token)
        user = await UserRepository().get_user_by_identifier(identifier)
        if user.subscriptions.gift.name == 'премиум-подписка':
            await User().refresh_subscription_user(identifier)
            user = await UserRepository().get_user_by_identifier(identifier)
        user_dict = user.to_read_model().dict()
        return JSONResponse(status_code=HTTPStatus.OK, content=user_dict)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка получения пользователя {e}")


