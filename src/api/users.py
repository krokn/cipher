from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Header
from loguru import logger
from starlette.responses import JSONResponse

from src.auth.utils import Auth
from src.schemas.users import UserByPhone
from src.services.core import User
from src.services.encryption import Encrypt

router = APIRouter(
    prefix="/api/user",
    tags=["Users"],
)


@router.get('')
async def get_user(token: str | None = Header(default=None)):
    try:
        identifier = Encrypt.get_user_by_token(token)
        user = await User().get_user(identifier)
        user_dict = user.dict()
        return JSONResponse(status_code=HTTPStatus.OK, content=user_dict)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка получения пользователя {e}")





# @router.post('/heart')
# async def add_hearts(phone: str):
#     try:
#         await User().add_hearts(phone, 5)
#         return JSONResponse(status_code=HTTPStatus.OK, content='Сердца добавлены')
#     except Exception as e:
#         logger.info(f'ошибка при добавлении сердец = {e}, телефон = {phone}')
#         raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка добавления сердец пользователю {e}")
#
#
# @router.post('/clue')
# async def add_clue(phone: str):
#     try:
#         await User().add_clue(phone, 1)
#         return JSONResponse(status_code=HTTPStatus.OK, content='Гаджеты добавлены')
#     except Exception as e:
#         logger.info(f'ошибка при добавлении гаджетов = {e}, телефон = {phone}')
#         raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"ошибка добавления гаджета пользователю {e}")
