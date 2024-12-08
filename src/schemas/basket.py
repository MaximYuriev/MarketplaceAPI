import uuid

from pydantic import BaseModel, Field, ConfigDict

from schemas.product import ProductBriefInfo


class BasketSchema(BaseModel):
    user_id: str | uuid.UUID
    basket_id: int


class AddProductOnBasketSchema(BaseModel):
    product_id: int
    product_count: int = Field(gt=0, lt=20, default=1)


class UpdateProductOnBasketSchema(BaseModel):
    product_count: int | None = Field(gt=0, lt=20, default=None)
    buy_in_next_order: bool | None = True


class ProductOnBasketSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product: ProductBriefInfo
    product_count: int = Field(serialization_alias="productCount")
    buy_in_next_order: bool = Field(serialization_alias="buyInNextOrder")


class OuterBasketSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    basket_id: int = Field(serialization_alias="basketId")
    products: list[ProductOnBasketSchema] = Field(validation_alias="product_on_basket")
