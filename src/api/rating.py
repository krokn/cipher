from http import HTTPStatus

from fastapi import APIRouter, Header, HTTPException
from loguru import logger
from starlette.responses import JSONResponse

from src.repositories.rating import RatingRepository
from src.repositories.users import UserRepository
from src.services.Changer import RatingChanger, UserChanger
from src.services.encryption import Encrypt

router = APIRouter(
    prefix="/api/rating",
    tags=["Rating"],
)


@router.post('/add_game')
async def add_game(token: str | None = Header(default=None), reputation_game: int = 0):
    try:
        phone = Encrypt.get_phone_by_token(token)
        logger.info(f'phone = {phone}')
        if phone is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="невалидный токен")
        else:
            await RatingChanger.update_reputation(phone, reputation_game)
            await UserChanger.update_current_level(phone)
            return JSONResponse(status_code=HTTPStatus.OK, content={"detail": "репутация обновлена"})
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка авторизации пользователя {e}")


