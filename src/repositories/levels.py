from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import get_async_session
from src.database.models import LevelModel, UserModel
from src.repositories.users import UserRepository
from src.schemas.levels import LevelSchema
from src.services.generate_levels import generate_new_levels
from src.utils.repository import SQLAlchemyRepository


class LevelsRepository(SQLAlchemyRepository):
    model = LevelModel

    @staticmethod
    async def get_next_level(current_level_id: int) -> LevelModel:
        async with get_async_session() as session:
            try:
                next_level_id = current_level_id + 1
                next_level_query = select(LevelModel).where(LevelModel.id == next_level_id)
                next_level_result = await session.execute(next_level_query)
                next_level = next_level_result.scalar_one_or_none()

                if not next_level:
                    await LevelsRepository().update_levels()
                    next_level_result = await session.execute(next_level_query)
                    next_level = next_level_result.scalar_one_or_none()

                    if not next_level:
                        raise NoResultFound(f"Level with ID {next_level_id} not found even after updating levels")
                return next_level
            except NoResultFound as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error fetching next level: {str(e)}")

    @staticmethod
    async def update_levels():
        new_levels = await generate_new_levels()
        await LevelsRepository().add_all(new_levels)
