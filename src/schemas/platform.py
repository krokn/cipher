from pydantic import BaseModel


class PlatfromSchema(BaseModel):
    id: int
    name: str