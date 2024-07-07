from http import HTTPStatus

from fastapi import HTTPException

from src.repositories.levels import LevelsRepository
from src.repositories.rating import RatingRepository
from src.repositories.users import UserRepository
from src.schemas.rating import RatingSchemaForAddUser
from src.schemas.users import UserSignUp
from src.services.сhanger import UserChanger, RatingChanger


class User:

    @staticmethod
    async def add_user(user: UserSignUp):
        user_dict = user.model_dump()
        user_id = await UserRepository().add_one(user_dict)
        rating = RatingSchemaForAddUser()
        rating_dict = rating.model_dump()
        rating_dict['user_id'] = user_id
        await RatingRepository().add_one(rating_dict)

    @staticmethod
    async def get_user(phone: str):
        return await UserRepository().get_user(phone)


class Level:

    @staticmethod
    async def get_level(phone: str):
        user = await UserRepository.get_user(phone)
        if user.hearts == 0:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Сердца закончились")
        else:
            user_from_rating = await RatingRepository().get_user_from_rating(user.id)
            level = await LevelsRepository().get_level(user_from_rating.current_level)
            await UserChanger().subtract_hearts(phone)
            level_dict = level.dict()
        return level_dict


class Rating:

    @staticmethod
    async def add_game(phone: str, reputation_game: int):
        try:
            await RatingChanger().update_reputation(phone, reputation_game)
            await UserChanger.update_current_level(phone)
        except Exception as e:
            return e

