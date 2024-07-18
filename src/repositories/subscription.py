from src.database.connection import get_async_session
from src.database.models import ModelGift, ModelSubscription
from src.utils.repository import SQLAlchemyRepository


class SubscriptionRepository(SQLAlchemyRepository):
    model = ModelSubscription
