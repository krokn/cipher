from http import HTTPStatus

from fastapi import APIRouter, Header, HTTPException
from starlette.responses import JSONResponse
from src.services.core import Level
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
        level_dict = await Level().get_level(phone)
    return JSONResponse(status_code=HTTPStatus.OK, content=level_dict)
