from src.repositories.rating import RatingRepository
from src.repositories.users import UserRepository
from src.schemas.rating import RatingSchemaForAddUser
from src.schemas.users import UserSignIn


class User:


    @staticmethod
    async def add_user(user: UserSignIn):
        user_dict = user.model_dump()
        user_id = await UserRepository().add_one(user_dict)
        rating = RatingSchemaForAddUser()
        rating_dict = rating.model_dump()
        rating_dict['user_id'] = user_id
        await RatingRepository().add_one(rating_dict)