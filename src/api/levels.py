from http import HTTPStatus

from fastapi import APIRouter, Header, HTTPException
from src.logging.logger import logger
from starlette.responses import JSONResponse
from src.services.core import Level
from src.services.encryption import Encrypt
from src.services.redis import redis_client

router = APIRouter(
    prefix="/api/levels",
    tags=["Levels"],
)


@router.get('')
async def get_level(token: str | None = Header(default=None)):
    try:
        identifier = Encrypt.get_user_by_token(token)
        if identifier is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="невалидный токен")
        level_dict = await Level().get_level(identifier)
        redis_client.set(identifier+'_level', 1, ex=1800)
        return JSONResponse(status_code=HTTPStatus.OK, content=level_dict)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f'error get level = {e}, identifier = {identifier}')
        raise HTTPException(status_code=500, detail=f"error get level: {e}")