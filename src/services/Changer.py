from loguru import logger

from src.repositories.rating import RatingRepository
from src.repositories.users import UserRepository


class RatingChanger:

    @staticmethod
    async def update_reputation(phone: str, reputation_game: int):
        user = await UserRepository().get_user(phone)
        logger.info(f'USER_ID = {user.id}')
        old_user_reputation = await RatingRepository().get_reputation_user(user.id)
        new_reputation = old_user_reputation + reputation_game
        await RatingRepository().update_reputation(user.id, new_reputation)


class UserChanger:

    @staticmethod
    async def subtract_hearts(phone):
        user = await UserRepository().get_user(phone)
        new_user_hersts = user.hearts - 1
        await UserRepository.update_heart_user(user.id, new_user_hersts)

    @staticmethod
    async def update_current_level(phone):
        user = await UserRepository().get_user(phone)
        user_from_rating = await RatingRepository().get_user_from_rating(user.id)
        new_current_level = user_from_rating.current_level + 1
        await RatingRepository().update_current_level(user.id, new_current_level)
