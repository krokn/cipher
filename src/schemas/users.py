from pydantic import BaseModel

from src.schemas.subscription import SubscriptionSchema


class UserSchema(BaseModel):
    id: int
    id_platform: int
    identifier: str
    hearts: int
    clue: int

    class Config:
        from_attributes = True


class UserByPhone(BaseModel):
    phone: str


class AuthEmail(BaseModel):
    email: str


class AuthEmailWithCode(AuthEmail):
    code: str


class UserSchemaDTORating(UserSchema):
    rating: "RatingSchema"


