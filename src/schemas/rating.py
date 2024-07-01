from typing import Optional

from pydantic import BaseModel, Field


class RatingSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    current_level: int
    reputation: int
    user_id: Optional[int] = Field(default=None)

    class Config:
        from_attributes = True


class RatingSchemaForAddUser(BaseModel):
    current_level: int = 1
    reputation: int = 0
    user_id: Optional[int] = Field(default=None)