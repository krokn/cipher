from pydantic import BaseModel


class GlobalSettingsSchema(BaseModel):
    key: str
    value: int