import uuid
from typing import Sequence

from fastapi import Depends

from models.product import Product
from repositories.product import ProductRepository
from schemas.product import ProductSchema, ProductUpdate


class ProductServices:
    def __init__(self, repository: ProductRepository = Depends()):
        self.repository = repository

    async def create(self, product_create: ProductSchema, user_id: uuid.UUID | str) -> Product:
        product_data = product_create.model_dump()
        product_data.update(user_id=user_id)
        return await self.repository.create(product_data)

    async def get(self, **kwargs) -> Product:
        return await self.repository.get(**kwargs)

    async def get_all_products(self, **kwargs) -> Sequence[Product]:
        return await self.repository.get_all(**kwargs)

    async def update(self, changed_product: Product, product_update: ProductUpdate) -> Product:
        update_product_data = product_update.model_dump(exclude_none=True)
        return await self.repository.update(changed_product, update_product_data)

    async def delete(self, deleted_product: Product):
        await self.repository.delete(deleted_product)

    def __repr__(self):
        return 'ProductService'