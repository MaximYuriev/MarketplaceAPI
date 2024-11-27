from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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

    async def get(self, **kwargs) -> Product | None:
        query = (
            select(Product)
            .options(selectinload(Product.added_by))
            .filter_by(**kwargs)
        )
        return await self.session.scalar(query)

    async def get_all(self, **kwargs) -> Sequence[Product]:
        query = (
            select(Product)
            .options(selectinload(Product.added_by))
            .filter_by(**kwargs)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, product: Product, product_data: dict) -> Product:
        print(product_data)
        for key, value in product_data.items():
            setattr(product, key, value)
        await self.session.commit()
        return product

    async def delete(self, product: Product):
        await self.session.delete(product)
        await self.session.commit()