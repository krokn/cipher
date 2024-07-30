from http import HTTPStatus

from fastapi import APIRouter, Header, HTTPException
from loguru import logger
from starlette.responses import JSONResponse
from src.services.core import Level
from src.services.encryption import Encrypt

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
        level_dict = await Level.get_level(identifier)
        return JSONResponse(status_code=HTTPStatus.OK, content=level_dict)
    except HTTPException as e:
        logger.error(f'HTTP error: {e.detail}, token: {token}')
        raise
    except Exception as e:
        logger.error(f'Unexpected error while getting level: {e}, token: {token}')
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка взятия уровня пользователю: {e}")