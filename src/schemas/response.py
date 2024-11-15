from pydantic import BaseModel

from schemas.product import ProductSchema


class ResponseModel(BaseModel):
    detail: str
    data: list | None = None

class ResponseProductModel(ResponseModel):
    data: ProductSchema | None = None