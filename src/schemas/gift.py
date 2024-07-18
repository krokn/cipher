import datetime

from pydantic import BaseModel


class GiftSchema(BaseModel):
    id: int
    name: str
    hearts: int
    clue: int



