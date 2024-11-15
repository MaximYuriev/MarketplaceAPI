from pydantic import BaseModel, Field


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
