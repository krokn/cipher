from abc import ABC, abstractmethod
from typing import List, Dict

from loguru import logger
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import aliased

from src.database.connection import get_async_session


class AbstractRepository(ABC):
  pass


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> int:
        async with get_async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def add_all(self, data_list: List[Dict]) -> List[int]:
        async with get_async_session() as session:
            stmt = insert(self.model).values(data_list).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().all()

    async def delete_all(self):
        async with get_async_session() as session:
            stmt = delete(self.model)
            await session.execute(stmt)
            await session.commit()

    async def find_by_param(self, where_criterion, where_search_param):
        async with get_async_session() as session:
            stmt = select(self.model).where(where_criterion == where_search_param)
            res = await session.execute(stmt)
            result = res.scalar_one_or_none()
            if result:
                return result.to_read_model()
            return None

    async def update_values(
            self, where_criterion, where_search_param,
            values_criterion, new_values
    ):
        async with get_async_session() as session:
            try:
                update_stmt = (
                    update(self.model)
                    .where(where_criterion == where_search_param)
                    .values({values_criterion: new_values})
                )
                await session.execute(update_stmt)
                await session.commit()
            except Exception as e:
                logger.error(f"Error adding game: {e}")
                return ()

    async def find_all(self, order_params):
        async with get_async_session() as session:
            stmt = select(self.model).order_by(order_params.desc())
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res
