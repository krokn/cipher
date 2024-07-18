from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.database.connection import get_async_session
from src.database.models import ModelGift, ModelUser, ModelSubscription
from src.repositories.gifts import GiftRepository
from src.repositories.levels import LevelsRepository
from src.repositories.platform import PlatformRepository
from src.repositories.rating import RatingRepository
from src.repositories.subscription import SubscriptionRepository
from src.repositories.users import UserRepository
from src.schemas.auth import AuthSchemaWithIdPlatform
from src.schemas.rating import RatingSchemaForAddUser
from src.schemas.subscription import SubscriptionSchema
from src.services.сhanger import UserChanger, RatingChanger


class User:

    @staticmethod
    async def add_user(identifier: str, platform: str):
        platform_db = await PlatformRepository().get_platform(platform)
        logger.info(f'platform_db = {platform_db}')
        user = AuthSchemaWithIdPlatform(identifier=identifier, id_platform=platform_db.id)
        user_dict = user.model_dump()
        user_id = await UserRepository().add_one(user_dict)
        subscription = SubscriptionSchema(user_id=user_id, gift_id=1)
        subscription_dict = subscription.dict()
        subscription_dict['updated_at'] = datetime.utcnow()
        await SubscriptionRepository().add_one(subscription_dict)
        rating = RatingSchemaForAddUser(user_id=user_id)
        rating_dict = rating.dict()
        await RatingRepository().add_one(rating_dict)

    @staticmethod
    async def get_user(identifier: str):
        return await UserRepository().get_user(identifier)

    @staticmethod
    async def add_gift(identifier: str, name_gift: str):
        gift = await GiftRepository().find_by_param(ModelGift.name, name_gift)
        await User().add_hearts_and_clue(identifier, gift.hearts, gift.clue)

    @staticmethod
    async def add_hearts_and_clue(identifier: str, number_of_hearts_to_add, number_of_clue_to_add):
        await UserChanger().plus_hearts(identifier, number_of_hearts_to_add)
        await UserChanger().plus_clue(identifier, number_of_clue_to_add)

    @staticmethod
    async def refresh_subscription(identifier: str):
        user = await User().get_user(identifier)
        subscription = await SubscriptionRepository().find_by_param(ModelSubscription.user_id, user.id)
        current_time = datetime.utcnow()
        last_updated_time = subscription.updated_at

        gift = await GiftRepository().find_by_param(ModelGift.id, subscription.gift_id)
        logger.info(f'gift = {gift.name}')

        if current_time - last_updated_time < timedelta(hours=23):
            raise HTTPException(status_code=400, detail="Подарок уже был получен")

        await User().add_gift(identifier, gift.name)

        await SubscriptionRepository().update_values(ModelSubscription.user_id, user.id, ModelSubscription.updated_at, current_time)

    @staticmethod
    async def add_hearts(phone: str, number_of_hearts_to_add):
        await UserChanger().plus_hearts(phone, number_of_hearts_to_add)

    @staticmethod
    async def add_clue(phone: str, number_of_clue_to_add):
        await UserChanger().plus_clue(phone, number_of_clue_to_add)

    @staticmethod
    async def subtract_clue(phone: str, number_of_clue_to_subtract):
        await UserChanger().subtract_clue(phone, number_of_clue_to_subtract)


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
