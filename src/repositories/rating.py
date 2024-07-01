from loguru import logger
from sqlalchemy import select, update

from src.database.connection import get_async_session
from src.database.models import Rating
from src.utils.repository import SQLAlchemyRepository


class RatingRepository(SQLAlchemyRepository):
    model = Rating

    async def add_game(self, user_id: int, new_reputation: int):
        async with get_async_session() as session:
            try:
                logger.info(f'user_id = {user_id}')
                update_stmt = (
                    update(self.model)
                    .where(self.model.user_id == user_id)
                    .values(reputation=new_reputation)
                )
                await session.execute(update_stmt)
                await session.commit()
            except Exception as e:
                logger.error(f"Error adding game: {e}")
                return ()

    async def get_reputation_user(self, user_id: int) -> int:
        async with get_async_session() as session:
            try:
                stmt = select(self.model).where(self.model.user_id == user_id)
                res = await session.execute(stmt)
                logger.info(f'res = {res}')
                res = res.scalar_one().to_read_model()
                user_reputation = res.reputation
                logger.info(f'user_reputation = {user_reputation}')
            except Exception as e:
                logger.error(f"Error retrieving user reputation: {e}")
                return() # Вернуть значение по умолчанию или обработать ошибку
            return user_reputation
