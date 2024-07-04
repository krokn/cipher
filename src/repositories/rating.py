from loguru import logger
from sqlalchemy import select, update

from src.database.connection import get_async_session
from src.database.models import Rating
from src.schemas.rating import RatingSchema
from src.schemas.users import UserSchema
from src.utils.repository import SQLAlchemyRepository


class RatingRepository(SQLAlchemyRepository):
    model = Rating

    @staticmethod
    async def update_reputation(user_id: int, new_reputation: int):
        rating = RatingRepository()
        res = await rating.update_values(Rating.user_id, user_id, Rating.reputation, new_reputation)
        return res

    @staticmethod
    async def update_current_level(user_id, new_current_level):
        rating = RatingRepository()
        await rating.update_values(Rating.user_id, user_id, Rating.current_level, new_current_level)

    @staticmethod
    async def find_all_rating_desc():
        rating = RatingRepository()
        await rating.find_all(Rating.reputation)



    async def get_user_from_rating(self, user_id: int) -> RatingSchema:
        async with get_async_session() as session:
            try:
                stmt = select(self.model).where(self.model.user_id == user_id)
                res = await session.execute(stmt)
                logger.info(f'res = {res}')
                res = res.scalar_one().to_read_model()
            except Exception as e:
                logger.error(f"Error retrieving user reputation: {e}")
                return (e)
            return res

    async def get_reputation_user(self, user_id: int) -> int:
        async with get_async_session() as session:
            try:
                logger.info(f'user_id = {user_id}')
                stmt = select(self.model).where(self.model.user_id == user_id)
                res = await session.execute(stmt)
                logger.info(f'res = {res}')
                res = res.scalar_one().to_read_model()
                user_reputation = res.reputation
                logger.info(f'user_reputation = {user_reputation}')
            except Exception as e:
                logger.error(f"Error retrieving user reputation: {e}")
                return ()  # Вернуть значение по умолчанию или обработать ошибку
            return user_reputation
