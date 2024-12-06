import datetime
import uuid

from pydantic import BaseModel, Field, ConfigDict, field_serializer

from schemas.product import ProductBriefInfo


class OrderProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product: ProductBriefInfo
    product_count: int = Field(serialization_alias="productOnOrderCount")
    product_on_order_price: int = Field(serialization_alias="productOnOrderPrice")


class OuterOrderSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    order_id: int = Field(serialization_alias="orderId")
    user_id: str | uuid.UUID = Field(serialization_alias="userId")
    full_price: int = Field(validation_alias="order_price", serialization_alias="fullPrice")
    created_at: datetime.datetime = Field(serialization_alias="createdAt")
    products: list[OrderProductSchema]

    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime.datetime):
        return created_at.strftime("%Y-%m-%d %H:%M:%S")