from pydantic import BaseModel, Field, ConfigDict

from schemas.user import UserOuterModel


class ProductSchema(BaseModel):
    name: str = Field(max_length=25)
    description: str
    price: int = Field(gt=0)
    quantity: int = Field(gt=0)


class ProductUpdate(ProductSchema):
    name: str | None = None
    description: str | None = None
    price: int | None = Field(gt=0, default=None)
    quantity: int | None = Field(gt=0, default=None)


class ProductInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_id: int = Field(serialization_alias="productId")
    name: str
    description: str
    price: int
    quantity: int
    in_stock: bool = Field(serialization_alias="inStock")
    added_by: UserOuterModel | None = Field(serialization_alias="addedBy")