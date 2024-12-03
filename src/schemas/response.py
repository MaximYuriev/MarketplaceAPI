from pydantic import BaseModel

from schemas.basket import OuterBasketSchema
from schemas.product import ProductSchema, ProductInfo


class ResponseModel(BaseModel):
    detail: str
    data: list | None = None


class ResponseProductModel(ResponseModel):
    data: ProductSchema | ProductInfo | list[ProductInfo]

class BasketResponse(ResponseModel):
    data: OuterBasketSchema