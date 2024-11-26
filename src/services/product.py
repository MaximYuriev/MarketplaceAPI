import uuid

from fastapi import Depends

from exceptions.product import ProductNotFound, ProductAlreadyExist, ProductNameNotUnique
from models.product import Product
from repositories.product import ProductRepository
from schemas.product import ProductSchema, ProductUpdate


class ProductServices:
    def __init__(self, repository: ProductRepository = Depends()):
        self.repository = repository

    async def create(self, product_create: ProductSchema, user_id: uuid.UUID | str) -> Product:
        product = await self.get_product_by_name(product_create.name)
        if product:
            raise ProductAlreadyExist
        product_data = product_create.model_dump()
        product_data.update(user_id=user_id)
        return await self.repository.create(product_data)

    async def get(self, product_id: int) -> Product:
        product = await self.repository.get(product_id)
        if product is None:
            raise ProductNotFound
        return product

    async def get_product_by_name(self, product_name: str) -> Product | None:
        return await self.repository.get_by_params(name=product_name)

    async def update(self, changed_product: Product, product_update: ProductUpdate) -> Product:
        if product_update.name:
            product = await self.get_product_by_name(product_update.name)
            if product:
                raise ProductNameNotUnique
        update_product_data = product_update.model_dump(exclude_none=True)
        return await self.repository.update(changed_product, update_product_data)

    async def delete(self, deleted_product: Product):
        await self.repository.delete(deleted_product)