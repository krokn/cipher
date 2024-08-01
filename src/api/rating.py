from http import HTTPStatus

from fastapi import APIRouter, Header, HTTPException
from loguru import logger
from starlette.responses import JSONResponse

from src.database.models import PlatformModel
from src.repositories.platform import PlatformRepository
from src.repositories.rating import RatingRepository
from src.responses.rating import response_rating
from src.services.core import Rating, User
from src.services.encryption import Encrypt

router = APIRouter(
    prefix="/api/rating",
    tags=["Rating"],
)


@router.post('/add_game')
async def add_game(token: str | None = Header(default=None), reputation_game: int = 0, used_clue: int = 0):
    try:
        identifier = Encrypt.get_user_by_token(token)
        await Rating().add_game(identifier, reputation_game, used_clue)
        return JSONResponse(status_code=HTTPStatus.OK, content="add reputation_game")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f'error add game = {e}, identifier = {identifier}')
        raise HTTPException(status_code=500, detail=f"error add game {e}, identifier = {identifier}")


@router.get('')
async def get_rating(token: str | None = Header(default=None), time: str = 'forever'):
    try:
        identifier = Encrypt.get_user_by_token(token)
        rating_orm = await RatingRepository().find_rating(identifier, time)
        if not rating_orm:
            return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content='rating not found')
        rating = response_rating(rating_orm, identifier)
        return JSONResponse(status_code=HTTPStatus.OK, content=rating)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error get rating = {e}, identifier = {identifier}")



