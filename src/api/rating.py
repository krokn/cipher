from fastapi import APIRouter, Header
from loguru import logger

from src.auth.utils import decode_base64
from src.repositories.rating import RatingRepository
from src.repositories.users import UserRepository

router = APIRouter(
    prefix="/api/rating",
    tags=["Rating"],
)


@router.post('/game')
async def add_game(token: str | None = Header(default=None), reputation_game: int = 0):
    encoded_phone = token.split("||")[0]
    phone = decode_base64(encoded_phone)
    user_db = await UserRepository().get_user(phone)
    old_user_reputation = await RatingRepository().get_reputation_user(user_db.id)
    new_reputation = old_user_reputation + reputation_game
    await RatingRepository().add_game(user_db.id, new_reputation)

