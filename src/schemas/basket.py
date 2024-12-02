import uuid

from pydantic import BaseModel


class BasketSchema(BaseModel):
    user_id: str | uuid.UUID
    basket_id: int
