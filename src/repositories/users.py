from loguru import logger
from sqlalchemy import select, update

from src.database.connection import get_async_session
from src.database.models import ModelUser
from src.schemas.users import UserSchema
from src.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = ModelUser

    @staticmethod
    async def get_user(phone: str) -> UserSchema:
        user_repository = UserRepository()
        res = await user_repository.find_by_param(ModelUser.phone, phone)
        return res

    @staticmethod
    async def update_heart_user(user_id: int, new_user_hearts):
        user = UserRepository()
        res = await user.update_values(ModelUser.id, user_id, ModelUser.hearts, new_user_hearts)
        return res

    @staticmethod
    async def update_clue_user(user_id: int, new_user_clue):
        user = UserRepository()
        res = await user.update_values(ModelUser.id, user_id, ModelUser.clue, new_user_clue)
        return res
