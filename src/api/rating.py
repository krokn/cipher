from http import HTTPStatus

from fastapi import APIRouter, Header, HTTPException
from loguru import logger
from starlette.responses import JSONResponse

from src.database.models import ModelPlatform
from src.repositories.platform import PlatformRepository
from src.repositories.rating import RatingRepository
from src.responses.rating import response_rating
from src.services.core import Rating, User
from src.services.сhanger import RatingChanger, UserChanger
from src.services.encryption import Encrypt

router = APIRouter(
    prefix="/api/rating",
    tags=["Rating"],
)


@router.post('/add_game')
async def add_game(token: str | None = Header(default=None), reputation_game: int = 0, used_clue: int = 0):
    try:
        identifier = Encrypt.get_user_by_token(token)
        if identifier is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="невалидный токен")
        else:
            await Rating().add_game(identifier, reputation_game)
            if used_clue != 0:
                await User().subtract_clue(identifier, used_clue)
            return JSONResponse(status_code=HTTPStatus.OK, content="репутация обновлена")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка авторизации пользователя {e}")


@router.get('')
async def get_rating(token: str | None = Header(default=None)):
    try:
        identifier = Encrypt.get_user_by_token(token)
        user = await User().get_user(identifier)
        platform = await PlatformRepository().find_by_param(ModelPlatform.id, user.id_platform)
        rating_orm = await RatingRepository().find_rating(platform.id)
        if not rating_orm:
            return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"Рейтинг не найден"})
        rating = response_rating(rating_orm)
        return JSONResponse(status_code=HTTPStatus.OK, content=rating)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка получения рейтинга {e}")



