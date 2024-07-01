from src.database.models import Level
from src.utils.repository import SQLAlchemyRepository


class LevelsRepository(SQLAlchemyRepository):
    model = Level