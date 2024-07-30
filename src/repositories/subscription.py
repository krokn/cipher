from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import get_async_session
from src.database.models import GiftModel, SubscriptionModel, UserModel
from src.utils.repository import SQLAlchemyRepository


class SubscriptionRepository(SQLAlchemyRepository):
    model = SubscriptionModel

    @staticmethod
    async def change_user_subscription(user: UserModel, gift: GiftModel):
        async with get_async_session() as session:
            try:
                user.subscriptions.gift_id = gift.id
                session.add(user)
                session.add(user.subscriptions)
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=500, detail=f"Error updating user subscription: {str(e)}")
