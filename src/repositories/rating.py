from typing import List

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import select, update, desc
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy.orm import joinedload

from src.database.connection import get_async_session, SyncSession
from src.database.models import RatingModelForever, UserModel, RatingModelWeek, RatingModelMonth
from src.repositories.levels import LevelsRepository
from src.repositories.users import UserRepository
from src.schemas.rating import RatingSchema, RatingSchemaDTO
from src.schemas.users import UserSchema
from src.utils.repository import SQLAlchemyRepository


class RatingRepository(SQLAlchemyRepository):
    model = RatingModelForever

    @staticmethod
    def reset_weekly_reputation():
        with SyncSession() as session:
            with session.begin():
                result = session.execute(select(RatingModelWeek))
                weekly_ratings = result.scalars().all()
                for rating in weekly_ratings:
                    rating.reputation = 0
                session.commit()

    @staticmethod
    def reset_monthly_reputation():
        with SyncSession() as session:
            with session.begin():
                result = session.execute(select(RatingModelMonth))
                monthly_ratings = result.scalars().all()
                for rating in monthly_ratings:
                    rating.reputation = 0
                session.commit()

    @staticmethod
    async def find_rating(identifier: int, time: str) -> List[RatingModelForever]:
        async with get_async_session() as session:
            user = await session.scalar(select(UserModel).where(UserModel.identifier == identifier))
            if time == 'week':
                query = (
                    select(RatingModelWeek)
                    .join(RatingModelWeek.user)
                    .options(joinedload(RatingModelWeek.user))
                    .filter(UserModel.id_platform == user.id_platform)
                    .order_by(desc(RatingModelWeek.reputation))
                )
                res = await session.execute(query)
            elif time == 'month':
                query = (
                    select(RatingModelMonth)
                    .join(RatingModelMonth.user)
                    .options(joinedload(RatingModelMonth.user))
                    .filter(UserModel.id_platform == user.id_platform)
                    .order_by(desc(RatingModelMonth.reputation))
                )
                res = await session.execute(query)
                pass
            else:
                query = (
                    select(RatingModelForever)
                    .join(RatingModelForever.user)
                    .options(joinedload(RatingModelForever.user))
                    .filter(UserModel.id_platform == user.id_platform)
                    .order_by(desc(RatingModelForever.reputation))
                )
                res = await session.execute(query)
                pass
            return res.scalars().all()

