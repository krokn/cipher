from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Header
from loguru import logger
from starlette.responses import JSONResponse

from src.auth.utils import Auth
from src.repositories.rating import RatingRepository
from src.repositories.users import UserRepository
from src.schemas.rating import RatingSchema, RatingSchemaForAddUser
from src.schemas.users import UserSignUp, UserSignIn
from src.services.users.users import User

router = APIRouter(
    prefix="/api/user",
    tags=["Users"],
)


@router.post('/signup')
async def signup(user: UserSignUp):
    try:
        await User.add_user(user)
        token = Auth.create_token(user.phone)
        return JSONResponse(status_code=HTTPStatus.OK, content=token)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка регистрации пользователя {e}")





