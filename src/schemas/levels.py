from pydantic import BaseModel


class LevelSchema(BaseModel):
    id: int
    code_length: int
    attempts: int
    degree_hint: int

    class Config:
        from_attributes = True