import random

from sqlalchemy import text

from src.database.connection import get_async_session
from src.database.models import Level
from src.repositories.levels import LevelsRepository


def generate_new_levels():
    NUMBER_LEVELS = 200
    new_levels = []
    for _ in range(NUMBER_LEVELS):
        new_levels.append({
            "code_length": random.randint(3, 7),
            "hint": random.randint(1, 5),
            "degree_hint": random.randint(1, 3)
        })
    return new_levels


async def update_levels():
    new_levels = generate_new_levels()
    await delete_old_levels()
    await restart_auto_increment()
    await LevelsRepository().add_all(new_levels)


async def delete_old_levels():
    await LevelsRepository().delete_all()


async def restart_auto_increment():
    async with get_async_session() as session:
        await session.execute(text("TRUNCATE TABLE levels RESTART IDENTITY;"))
        await session.commit()
