from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Header
from starlette.responses import JSONResponse

from src.auth.utils import Auth
from src.schemas.users import UserSignUp
from src.services.core import User
from src.services.encryption import Encrypt

router = APIRouter(
    prefix="/api/user",
    tags=["Users"],
)


@router.post('/signup')
async def signup(user: UserSignUp):
    try:
        await User().add_user(user)
        token = Auth.create_token(user.phone)
        return JSONResponse(status_code=HTTPStatus.OK, content=token)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка регистрации пользователя {e}")


@router.get('')
async def get_user(token: str | None = Header(default=None)):
    try:
        phone = Encrypt.get_phone_by_token(token)
        user = await User().get_user(phone)
        user_dict = user.dict()
        return JSONResponse(status_code=HTTPStatus.OK, content=user_dict)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка получения пользователя {e}")
