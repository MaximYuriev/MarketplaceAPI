from pydantic import BaseModel

from schemas.balance import OuterBalanceSchema
from schemas.basket import OuterBasketSchema
from schemas.order import OuterOrderSchema
from schemas.product import ProductSchema, ProductInfo


class ResponseModel(BaseModel):
    detail: str
    data: list | int | None = None


class ResponseProductModel(ResponseModel):
    data: ProductSchema | ProductInfo | list[ProductInfo]


class BasketResponse(ResponseModel):
    data: OuterBasketSchema


class OrderResponse(ResponseModel):
    data: OuterOrderSchema | list[OuterOrderSchema]


class BalanceResponse(ResponseModel):
    data: OuterBalanceSchema