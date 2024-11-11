import uuid

from pydantic import BaseModel, Field, computed_field, field_validator

from auth.config import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE


class BaseTokenPayload(BaseModel):
    sub: str = Field(validation_alias="user_id")

    @field_validator("sub", mode='before')
    @classmethod
    def validate_sub(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        raise ValueError("Тип объекта должен быть UUID")


class RefreshTokenPayload(BaseTokenPayload):
    type: str = Field(default=REFRESH_TOKEN_TYPE)


class AccessTokenPayload(BaseTokenPayload):
    type: str = Field(default=ACCESS_TOKEN_TYPE)
    email: str
    firstname: str = Field(exclude=True)
    surname: str = Field(exclude=True)
    role: int = Field(validation_alias="user_role")

    @computed_field
    def name(self) -> str:
        return f"{self.firstname} {self.surname}"

