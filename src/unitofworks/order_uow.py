from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from repositories.basket_product import BasketProductRepository
from repositories.order import OrderRepository
from repositories.order_product import OrderProductRepository
from repositories.product import ProductRepository


class OrderBasketWork:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    async def __aenter__(self):
        self.order_repository = OrderRepository(self.session)
        self.order_product_repository = OrderProductRepository(self.session)
        self.basket_product_repository = BasketProductRepository(self.session)
        self.product_repository = ProductRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()