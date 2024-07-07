from http import HTTPStatus

from fastapi import APIRouter, Header, HTTPException
from loguru import logger
from starlette.responses import JSONResponse

from src.repositories.rating import RatingRepository
from src.responses.rating import response_raiting
from src.services.core import Rating
from src.services.сhanger import RatingChanger, UserChanger
from src.services.encryption import Encrypt

router = APIRouter(
    prefix="/api/rating",
    tags=["Rating"],
)


@router.post('/add_game')
async def add_game(token: str | None = Header(default=None), reputation_game: int = 0):
    try:
        phone = Encrypt.get_phone_by_token(token)
        if phone is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="невалидный токен")
        else:
            await Rating().add_game(phone, reputation_game)
            return JSONResponse(status_code=HTTPStatus.OK, content={"репутация обновлена"})
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка авторизации пользователя {e}")


@router.get('')
async def get_rating():
    try:
        rating_orm = await RatingRepository().find_all_relationship()
        if not rating_orm:
            return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"Рейтинг не найден"})
        rating = response_raiting(rating_orm)
        return JSONResponse(status_code=HTTPStatus.OK, content=rating)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка получения рейтинга {e}")



