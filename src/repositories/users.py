from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload, joinedload

from src.database.connection import get_async_session
from src.database.models import UserModel, GiftModel, SubscriptionModel

from src.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = UserModel

    @staticmethod
    async def get_user_by_identifier(
            identifier: str,
            include: Optional[List[str]] = None
    ) -> Optional[UserModel]:
        async with get_async_session() as session:
            try:
                query = select(UserModel).where(UserModel.identifier == identifier)

                if include:
                    if 'level' in include:
                        query = query.options(joinedload(UserModel.level_rel))
                    if 'subscriptions' in include:
                        query = query.options(joinedload(UserModel.subscriptions))
                    if 'gift' in include:
                        query = query.options(
                            joinedload(UserModel.subscriptions).joinedload(SubscriptionModel.gift)
                        )
                    if 'rating' in include:
                        query = query.options(
                            joinedload(UserModel.rating_forever),
                            joinedload(UserModel.rating_week),
                            joinedload(UserModel.rating_month)
                        )

                query_result = await session.execute(query)
                user = query_result.scalar_one_or_none()
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
    async def save_user(
            user: UserModel,
            include: Optional[List[str]] = None
    ):
        async with get_async_session() as session:
            async with session.begin():
                try:
                    session.add(user)

                    if include:
                        if 'subscriptions' in include and user.subscriptions:
                            session.add(user.subscriptions)
                            if 'gifts' in include and user.subscriptions.gift:
                                session.add(user.subscriptions.gift)
                        if 'rating_forever' in include and user.rating_forever:
                            session.add(user.rating_forever)
                        if 'rating_week' in include and user.rating_week:
                            session.add(user.rating_week)
                        if 'rating_month' in include and user.rating_month:
                            session.add(user.rating_month)
                        if 'level' in include and user.level_rel:
                            session.add(user.level_rel)

                    await session.flush()
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    raise HTTPException(status_code=500, detail=f"Error saving user: {str(e)}")
