from typing import List

from loguru import logger
from sqlalchemy import select, update, desc
from sqlalchemy.orm import joinedload

from src.database.connection import get_async_session
from src.database.models import ModelRating
from src.schemas.rating import RatingSchema, RatingSchemaDTO
from src.schemas.users import UserSchema
from src.utils.repository import SQLAlchemyRepository


class RatingRepository(SQLAlchemyRepository):
    model = ModelRating

    # @staticmethod
    # async def select_with_relationship():
    #     async with get_async_session() as session:
    #         query = (
    #             select(Rating)
    #             .options(joinedload(Rating.user))
    #         )
    #         res = await session.execute(query)
    #         print(res)
    #         result = res.scalars().first()
    #         result_dto = RatingSchemaDTO.model_validate(result, from_attributes=True)
    #         print(result_dto)
    #         print(result_dto.user.phone)

    @staticmethod
    async def update_reputation(user_id: int, new_reputation: int):
        rating = RatingRepository()
        res = await rating.update_values(ModelRating.user_id, user_id, ModelRating.reputation, new_reputation)
        return res

    @staticmethod
    async def update_current_level(user_id, new_current_level):
        rating = RatingRepository()
        await rating.update_values(ModelRating.user_id, user_id, ModelRating.current_level, new_current_level)

    @staticmethod
    async def find_all_rating_desc():
        rating = RatingRepository()
        return await rating.find_all(ModelRating.reputation)

    @staticmethod
    async def find_all_relationship() -> List[ModelRating]:
        async with get_async_session() as session:
            query = select(ModelRating).options(joinedload(ModelRating.user)).order_by(desc(ModelRating.reputation))
            res = await session.execute(query)
            return res.scalars().all()

    async def get_user_from_rating(self, user_id: int):
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
