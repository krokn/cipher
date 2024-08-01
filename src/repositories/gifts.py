from fastapi import HTTPException
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import get_async_session
from src.database.models import GiftModel
from src.utils.repository import SQLAlchemyRepository


class GiftRepository(SQLAlchemyRepository):
    model = GiftModel

    @staticmethod
    async def get_gift_by_name(gift_name: str):
        async with get_async_session() as session:
            result = await session.execute(select(GiftModel).where(GiftModel.name == gift_name))
            gift = result.scalar()
            if not gift:
                raise HTTPException(status_code=404, detail="gift not found")
            return gift

