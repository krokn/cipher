from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


from src.database.connection import get_async_session
from src.database.models import UserModel, GiftModel

from src.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = UserModel

    @staticmethod
    async def get_user_by_identifier(identifier: str) -> UserModel:
        async with get_async_session() as session:
            try:
                query = await session.execute(select(UserModel).where(UserModel.identifier == identifier))
                user = query.scalar_one_or_none()
                return user
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

    @staticmethod
    async def add_gift(user: UserModel, gift: GiftModel):
        async with get_async_session() as session:
            try:

                user.hearts += gift.hearts
                user.clue += gift.clue
                session.add(user)

                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=500, detail=f"Error updating user with gift: {str(e)}")

    @staticmethod
    async def save_user(user: UserModel):
        async with get_async_session() as session:
            try:
                session.add(user)
                session.add(user.subscriptions)
                session.add(user.rating_forever)
                session.add(user.rating_week)
                session.add(user.rating_month)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=500, detail=f"Error saving user: {str(e)}")



