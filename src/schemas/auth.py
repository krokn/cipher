from pydantic import BaseModel, field_validator, EmailStr


class AuthSchemaWithPhone(BaseModel):
    identifier: str
    platform: str

    @field_validator('identifier')
    def validate_phone(cls, value):
        if not (value.startswith('+') and value[1:].isdigit()):
            raise ValueError('Phone number must start with "+" and contain only digits.')
        return value


class AuthSchemaWithEmail(BaseModel):
    identifier: EmailStr
    platform: str


class AuthSchemaWithIdPlatform(BaseModel):
    identifier: str
    id_platform: id

    class Config:
        arbitrary_types_allowed = True


class AuthSchemaForAddUser(BaseModel):
    identifier: str
