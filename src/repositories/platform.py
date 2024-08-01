from fastapi import HTTPException
from loguru import logger
from sqlalchemy import select

from src.database.connection import get_async_session
from src.database.models import PlatformModel, LevelModel
from src.utils.repository import SQLAlchemyRepository


class PlatformRepository(SQLAlchemyRepository):
    model = PlatformModel

    @staticmethod
    async def get_platform(platform_name: str):
        async with get_async_session() as session:
            result = await session.execute(select(PlatformModel).where(PlatformModel.name == platform_name))
            platform = result.scalar_one_or_none()
            if not platform:
                raise HTTPException(status_code=404, detail="platform not found")
            return platform


