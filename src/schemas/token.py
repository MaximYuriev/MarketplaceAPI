import uuid

from pydantic import BaseModel, Field, computed_field, field_validator

from auth.config import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from schemas.basket import BasketSchema


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
    basket_schema: BasketSchema = Field(exclude=True, validation_alias="basket")

    @computed_field
    def name(self) -> str:
        return f"{self.firstname} {self.surname}"

    @computed_field
    def basket(self) -> int:
        return self.basket_schema.basket_id
