from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Header
from loguru import logger

from src.auth.utils import create_token, decode_base64
from src.repositories.rating import RatingRepository
from src.repositories.users import UserRepository
from src.schemas.rating import RatingSchema, RatingSchemaForAddUser
from src.schemas.users import UserSignUp, UserSignIn

router = APIRouter(
    prefix="/api/user",
    tags=["Users"],
)


@router.post('/signup')
async def signup(user: UserSignUp):
    user_dict = user.model_dump()
    user_id = await UserRepository().add_one(user_dict)
    rating = RatingSchemaForAddUser()
    rating_dict = rating.model_dump()
    logger.info(f'rating_dict = {rating_dict}')
    rating_dict['user_id'] = user_id
    await RatingRepository().add_one(rating_dict)
    raise HTTPException(status_code=HTTPStatus.OK, detail=f"{user_id}")


@router.post('/signin')
async def signin(user: UserSignIn):
    user_db = await UserRepository().get_user(user.phone)
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="пользователь с таким номером не найден")
    else:
        raise HTTPException(status_code=HTTPStatus.OK, detail=f"{create_token(user.phone)}")



