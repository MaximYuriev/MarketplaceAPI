import uuid
from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserLogin):
    firstname: Annotated[str, MinLen(3), MaxLen(20)]
    surname: Annotated[str, MinLen(3), MaxLen(20)]
    password: Annotated[str, MinLen(7), MaxLen(15)]


class UserPayload(BaseModel):
    user_id: str = Field(validation_alias="sub")
    email: str
    name: str
    role_id: int = Field(validation_alias="role")


class UserOuterModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: str = Field(serialization_alias="userId")
    firstname: str
    surname: str

    @field_validator("user_id", mode='before')
    @classmethod
    def validate_sub(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        raise ValueError("Тип объекта должен быть UUID")
