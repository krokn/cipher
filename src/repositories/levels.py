from sqlalchemy import select

from src.database.connection import get_async_session
from src.database.models import ModelLevel
from src.schemas.levels import LevelSchema
from src.utils.repository import SQLAlchemyRepository


class LevelsRepository(SQLAlchemyRepository):
    model = ModelLevel

    async def get_level(self, level_id: str) -> LevelSchema:
        async with get_async_session() as session:
            stmt = select(self.model).where(self.model.id == level_id)
            res = await session.execute(stmt)
            res = res.scalar_one().to_read_model()
            return res