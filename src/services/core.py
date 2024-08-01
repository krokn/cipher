from datetime import timedelta, datetime as time
import time as Time
from fastapi import HTTPException
from loguru import logger
from src.database.models import UserModel, PlatformModel, GiftModel, SubscriptionModel, RatingModelWeek, \
    RatingModelMonth, RatingModelForever
from src.repositories.gifts import GiftRepository

from src.repositories.levels import LevelsRepository
from src.repositories.platform import PlatformRepository
from src.repositories.subscription import SubscriptionRepository

from src.repositories.users import UserRepository


class User:

    @staticmethod
    async def add_user(identifier: str, platform: str):
        if await UserRepository().get_user_by_identifier(identifier) is not None:
            raise HTTPException(status_code=403, detail=f"user register, can login")
        gift = await GiftRepository().get_gift_by_name('обычная-подписка')
        platform = await PlatformRepository().get_platform(platform)
        user = User().create_user(identifier, platform, gift)
        await UserRepository().save_user(user, include=['rating_forever', 'rating_week', 'rating_month', 'subscriptions', 'gifts', 'level'])

    @staticmethod
    async def add_gift_user(identifier: str, name_gift: str):
        gift = await GiftRepository().get_gift_by_name(name_gift)
        user = await UserRepository().get_user_by_identifier(identifier, include=['subscriptions', 'gift'])
        await UserRepository().add_gift(user, gift)

    @staticmethod
    async def change_subscribe_user(identifier: str, name_gift: str):
        gift = await GiftRepository().get_gift_by_name(name_gift)
        user = await UserRepository().get_user_by_identifier(identifier, include=['subscriptions', 'gift'])
        user = User().update_subscription(user)
        await SubscriptionRepository().change_user_subscription(user, gift)
        await UserRepository().save_user(user, include=['subscriptions', 'gifts'])

    @staticmethod
    async def refresh_subscription_user(identifier: str):
        user_from_db = await UserRepository().get_user_by_identifier(identifier, include=['subscriptions', 'gift'])
        days = 1
        if user_from_db.subscriptions.gift.name == 'премиум-подписка':
            days = User().check_subscription_update_time_for_prime_user(user_from_db)
            if days is None:
                return
        elif user_from_db.subscriptions.gift.name == 'обычная-подписка':
            User().check_subscription_update_time(user_from_db)
        user = User().update_subscription(user_from_db, days)
        await UserRepository().save_user(user, include=['subscriptions'])

    @staticmethod
    def update_subscription(user: UserModel, days: int = 1):
        try:
            current_time = time.now()
            user.hearts += user.subscriptions.gift.hearts * days
            user.clue += user.subscriptions.gift.clue * days
            user.subscriptions.updated_at = current_time
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating user with subscription: {str(e)}")

    @staticmethod
    def check_subscription_update_time(user: UserModel):
        current_time = time.now()
        last_updated_time = user.subscriptions.updated_at
        difference_in_time = current_time - last_updated_time
        if difference_in_time < timedelta(hours=23):
            raise HTTPException(status_code=401, detail="Подарок уже был получен")

    @staticmethod
    def check_subscription_update_time_for_prime_user(user: UserModel):
        current_time = time.now()
        last_updated_time = user.subscriptions.updated_at
        difference_in_time = (current_time - last_updated_time).days
        logger.info(f'current_time - last_updated_time = {difference_in_time}')
        if difference_in_time > 0:
            return difference_in_time

    @staticmethod
    def update_user_ratings_and_level(user: UserModel, reputation_game: int, used_clue: int, next_level_id: int):
        try:
            user.rating_forever.reputation += reputation_game
            user.rating_week.reputation += reputation_game
            user.rating_month.reputation += reputation_game
            user.level_id = next_level_id
            user.clue -= used_clue
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating user ratings and level: {str(e)}")

    @staticmethod
    def create_user(identifier: str, platform: PlatformModel, gift: GiftModel):
        try:
            subscriptions = SubscriptionModel(gift_id=gift.id)
            rating_week = RatingModelWeek()
            rating_month = RatingModelMonth()
            rating_forever = RatingModelForever()

            user = UserModel(
                identifier=identifier,
                hearts=gift.hearts,
                clue=gift.clue,
                id_platform=platform.id,
                platform=platform,
                subscriptions=subscriptions,
                rating_week=rating_week,
                rating_month=rating_month,
                rating_forever=rating_forever
            )
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"error creating user {e}")


class Level:

    @staticmethod
    async def get_level(identifier: str):
        try:
            user = await UserRepository().get_user_by_identifier(identifier, include=['level'])
            if not user.level_rel:
                await LevelsRepository().update_levels()
                user = await UserRepository().get_user_by_identifier(identifier, include=['level'])

            level = user.level_rel
            if user.hearts == 0:
                raise HTTPException(status_code=402, detail=f"hearts are over")
            else:
                user.hearts -= 1
                level_dict = level.to_read_model().dict()
                await UserRepository().save_user(user)
                return level_dict
        except Exception as e:
            logger.error(f'Unexpected error: {e}')
            raise HTTPException(status_code=500, detail=f"error: {e}")


class Rating:

    @staticmethod
    async def add_game(identifier: str, reputation_game: int, used_clue: int):
        user = await UserRepository().get_user_by_identifier(identifier, include=['rating', 'level'])
        if reputation_game == 0:
            id_level_to_add = user.level_id
        else:
            next_level = await LevelsRepository().get_next_level(user.level_id)
            id_level_to_add = next_level.id
        User().update_user_ratings_and_level(user, reputation_game, used_clue, id_level_to_add)
        await UserRepository().save_user(user, include=['rating_forever', 'rating_week', 'rating_month', 'level'])
