from abc import ABC, abstractmethod
from typing import List, Dict

from loguru import logger
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import aliased

from src.database.connection import get_async_session


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError


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

    @staticmethod
    async def left_join(self, join_model, join_criterion, select_columns, where_criterion=None,
                        where_search_param=None):
        async with get_async_session() as session:
            try:
                aliased_join_model = aliased(join_model)
                stmt = (
                    select(select_columns)
                    .select_from(self.model)
                    .join(aliased_join_model, join_criterion, isouter=True)
                )

                if where_criterion and where_search_param:
                    stmt = stmt.where(where_criterion == where_search_param)

                res = await session.execute(stmt)
                results = res.fetchall()
                logger.info(f'results = {results}')
                return results
            except Exception as e:
                logger.error(f"Error performing left join: {e}")
                return None


    async def find_all(self):
        async with get_async_session() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res
