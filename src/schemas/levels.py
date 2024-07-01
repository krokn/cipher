from pydantic import BaseModel


class LevelSchema(BaseModel):
    id: int
    code_length: int
    hint: int
    degree_hint: int

    class Config:
        from_attributes = True