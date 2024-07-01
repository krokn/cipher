from loguru import logger
from sqlalchemy import select

from src.database.connection import get_async_session
from src.database.models import User
from src.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_user(self, phone: str) -> tuple:
        async with get_async_session() as session:
            try:
                logger.info(f'phone = {phone}')
                stmt = select(self.model).where(self.model.phone == phone)
                res = await session.execute(stmt)
                res = res.scalar_one().to_read_model()
                logger.info(f'res = {res}')
            except Exception as e:
                res = []
            return res
