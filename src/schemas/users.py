from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    phone: str
    subscription_status: bool
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


class UserSchemaDTO(UserSchema):
    rating: "RatingSchema"
