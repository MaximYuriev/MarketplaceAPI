from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, Field


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