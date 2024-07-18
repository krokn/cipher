from sqlalchemy import select

from src.database.connection import get_async_session
from src.database.models import ModelGift
from src.utils.repository import SQLAlchemyRepository


class GiftRepository(SQLAlchemyRepository):
    model = ModelGift


