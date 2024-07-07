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
    async def update_heart_user(user_id, new_current_level):
        user = UserRepository()
        res = await user.update_values(ModelUser.id, user_id, ModelUser.hearts, new_current_level)
        return res
