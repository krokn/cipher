from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    phone: str
    subscription_status: bool
    hearts: int
    clue: int

    class Config:
        from_attributes = True


class UserSignUp(BaseModel):
    phone: str


class UserSchemaDTO(UserSchema):
    rating: "RatingSchema"
