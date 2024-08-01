import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Annotated

from loguru import logger
from sqlalchemy import MetaData, String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SYNC_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
logger.info(f'DATABASE_URL = {DATABASE_URL}')
logger.info(f'SYNC_DATABASE_URL = {SYNC_DATABASE_URL}')


str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 10
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


metadata = MetaData()

sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
SyncSession = sessionmaker(bind=sync_engine, autoflush=False, expire_on_commit=False)

engine = create_async_engine(DATABASE_URL, echo=True, )
async_session_maker = async_sessionmaker(engine)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
