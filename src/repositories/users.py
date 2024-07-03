from loguru import logger
from sqlalchemy import select, update

from src.database.connection import get_async_session
from src.database.models import User
from src.schemas.users import UserSchema
from src.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    @staticmethod
    async def get_user(phone: str) -> UserSchema:
        user_repository = UserRepository()
        res = await user_repository.find_by_param(User.phone, phone)
        return res

    @staticmethod
    async def update_heart_user(user_id, new_current_level):
        user = UserRepository()
        res = await user.update_values(User.id, user_id, User.hearts, new_current_level)
        return res
