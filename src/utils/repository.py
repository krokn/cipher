from abc import ABC, abstractmethod
from typing import List, Dict

from loguru import logger
from sqlalchemy import insert, select, delete

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

    async def find_all(self):
        async with get_async_session() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res
