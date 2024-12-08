from typing import Annotated

from fastapi import Depends

from models.basket import BasketProduct
from repositories.basket_product import BasketProductRepository
from schemas.basket import AddProductOnBasketSchema, UpdateProductOnBasketSchema


class BasketProductService:
    def __init__(self, repository: Annotated[BasketProductRepository, Depends(BasketProductRepository)]):
        self.repository = repository

    async def add_product(self, basket_id: int, product: AddProductOnBasketSchema):
        add_data = product.model_dump()
        add_data.update(basket_id=basket_id)
        await self.repository.create(add_data)

    async def get_one(self, **kwargs) -> BasketProduct | None:
        return await self.repository.get_one_by_params(**kwargs)

    async def update(self, basket_product: BasketProduct, product: UpdateProductOnBasketSchema):
        update_data = product.model_dump(exclude_none=True)
        await self.repository.update(basket_product, update_data)

    async def delete(self, basket_product: BasketProduct):
        await self.repository.delete(basket_product)
