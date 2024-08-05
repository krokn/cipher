from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Header
from src.logging.logger import logger
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
        user = await UserRepository().get_user_by_identifier(identifier, include=['subscriptions', 'gift'])
        if user.subscriptions.gift.name == 'премиум-подписка':
            await User().refresh_subscription_user(identifier)
            user = await UserRepository().get_user_by_identifier(identifier)
        user_dict = user.to_read_model().dict()
        return JSONResponse(status_code=HTTPStatus.OK, content=user_dict)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error get user = {e}, identifier = {identifier}")


@router.post('')
async def subtract_clue(token: str | None = Header(default=None), used_clue: int = 0):
    try:
        identifier = Encrypt.get_user_by_token(token)
        await User().subtract_clue_user(identifier, used_clue)
        return JSONResponse(status_code=HTTPStatus.OK, content='subtract clue')
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error subtract clue = {e}, identifier = {identifier}")
