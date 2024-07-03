from http import HTTPStatus

from fastapi import APIRouter, Header, HTTPException
from starlette.responses import JSONResponse

from src.repositories.levels import LevelsRepository
from src.repositories.rating import RatingRepository
from src.repositories.users import UserRepository
from src.schemas.levels import LevelSchema
from src.services.Changer import UserChanger
from src.services.encryption import Encrypt

router = APIRouter(
    prefix="/api/levels",
    tags=["Levels"],
)


@router.get('')
async def get_level(token: str | None = Header(default=None)):
    phone = Encrypt.get_phone_by_token(token)
    if phone is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="невалидный токен")
    else:
        user = await UserRepository.get_user(phone)
        if user.hearts == 0:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Сердца закончились")
        else:
            user_from_rating = await RatingRepository().get_user_from_rating(user.id)
            level = await LevelsRepository().get_level(user_from_rating.current_level)
            await UserChanger().subtract_hearts(phone)
            level_json = level.dict()
    return JSONResponse(status_code=HTTPStatus.OK, content=level_json)
