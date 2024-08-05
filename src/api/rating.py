from http import HTTPStatus

from fastapi import APIRouter, Header, HTTPException
from src.logging.logger import logger
from starlette.responses import JSONResponse

from src.database.models import PlatformModel
from src.repositories.platform import PlatformRepository
from src.repositories.rating import RatingRepository
from src.responses.rating import response_rating
from src.services.core import Rating, User
from src.services.encryption import Encrypt
from src.services.redis import redis_client

router = APIRouter(
    prefix="/api/rating",
    tags=["Rating"],
)


@router.post('/add_game')
async def add_game(token: str | None = Header(default=None), reputation_game: int = 0):
    try:
        identifier = Encrypt.get_user_by_token(token)
        isGetLevel = redis_client.get(identifier + '_level')
        if isGetLevel and reputation_game < 100:
            await Rating().add_game(identifier, reputation_game)
            redis_client.delete(identifier + '_level')
            logger.info(f'user = {identifier} add reputation = {reputation_game}')
            return JSONResponse(status_code=HTTPStatus.OK, content="add reputation game")
        else:
            logger.error(f'user = {identifier} is cheating')
            redis_client.delete(identifier + '_level')
            raise HTTPException(status_code=409, detail=f'user = {identifier} is cheating')
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



