from pydantic import BaseModel

from schemas.product import ProductSchema, ProductInfo


class ResponseModel(BaseModel):
    detail: str
    data: list | None = None


class ResponseProductModel(ResponseModel):
    data: ProductSchema | ProductInfo | list[ProductInfo] | None = None
