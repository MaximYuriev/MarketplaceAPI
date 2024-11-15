from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from models.product import Product


class ProductRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create(self, product_data: dict) -> Product:
        product = Product(**product_data)
        self.session.add(product)
        await self.session.commit()
        return product

    async def get(self, product_id: int) -> Product | None:
        return await self.session.get(Product, product_id)

    async def get_by_params(self, **kwargs) -> Product | None:
        query = select(Product).filter_by(**kwargs)
        return await self.session.scalar(query)

    async def update(self, product: Product, product_data: dict):
        for key, value in product_data.items():
            setattr(product, key, value)
        await self.session.commit()

    async def delete(self, product: Product):
        await self.session.delete(product)
        await self.session.commit()