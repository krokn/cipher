from sqlalchemy import select

from src.database.connection import get_async_session
from src.database.models import GlobalSettings
from src.schemas.settings import GlobalSettingsSchema
from src.utils.repository import SQLAlchemyRepository


class AdminRepository(SQLAlchemyRepository):
    model = GlobalSettings

    async def get_all(self) -> list[GlobalSettingsSchema]:
        async with get_async_session() as session:
            query = select(self.model)
            db_res = await session.execute(query)
            res = [row[0].to_read_model() for row in db_res.all()]
            return res
