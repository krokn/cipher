from src.database.models import ModelPlatform
from src.schemas.platform import PlatfromSchema
from src.utils.repository import SQLAlchemyRepository


class PlatformRepository(SQLAlchemyRepository):
    model = ModelPlatform

    @staticmethod
    async def get_platform(name: str) -> PlatfromSchema:
        platform_repository = PlatformRepository()
        res = await platform_repository.find_by_param(ModelPlatform.name, name)
        return res
