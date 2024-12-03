import uuid

from pydantic import BaseModel, Field, ConfigDict

from schemas.product import ProductInfo


class BasketSchema(BaseModel):
    user_id: str | uuid.UUID
    basket_id: int


class AddProductOnBasketSchema(BaseModel):
    product_id: int
    product_count: int = Field(gt=0, lt=20, default=1)


class UpdateProductOnBasketSchema(BaseModel):
    product_count: int = Field(gt=0, lt=20, default=1)


class ProductOnBasketSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_id: int = Field(serialization_alias="productId")
    product_count: int = Field(serialization_alias="productCount")
    product: ProductInfo


class OuterBasketSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    basket_id: int = Field(serialization_alias="basketId")
    products: list[ProductOnBasketSchema] = Field(validation_alias="product_on_basket")
