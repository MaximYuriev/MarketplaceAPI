from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db import get_session
from models.basket import BasketProduct, Basket
from models.product import Product


class BasketProductRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    async def create(self, add_data: dict):
        basket_product = BasketProduct(**add_data)
        self.session.add(basket_product)
        await self.session.commit()

    async def get_products(self, basket_id: int) -> Basket | None:
        return await self.session.get(
            Basket,
            basket_id,
            options=[
                selectinload(Basket.product_on_basket)
                .selectinload(BasketProduct.product)
                .selectinload(Product.added_by)
            ]
        )

    async def get_one_by_params(self, **kwargs) -> BasketProduct | None:
        query = select(BasketProduct).filter_by(**kwargs)
        return await self.session.scalar(query)

    async def get_all_by_params(self, **kwargs) -> Sequence[BasketProduct]:
        query = select(BasketProduct).options(selectinload(BasketProduct.product)).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, basket_product: BasketProduct, update_product_data: dict):
        for key, value in update_product_data.items():
            setattr(basket_product, key, value)
        await self.session.commit()

    async def delete(self, basket_product: BasketProduct):
        await self.session.delete(basket_product)
        await self.session.commit()
