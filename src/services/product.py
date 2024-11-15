import uuid

from fastapi import Depends

from exceptions.product import ProductNotFound, ProductAlreadyExist
from models.product import Product
from repositories.product import ProductRepository
from schemas.product import ProductSchema


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