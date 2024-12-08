import uuid
from typing import Annotated

from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, with_loader_criteria

from db import get_session
from models.basket import Basket, BasketProduct


class BasketRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    def create(self, user_id: uuid.UUID | str):
        basket = Basket(user_id=user_id)
        self.session.add(basket)

    async def get_products(self, basket_id: int) -> Basket | None:
        return await self.session.get(
            Basket,
            basket_id,
            options=[
                selectinload(Basket.product_on_basket)
                .selectinload(BasketProduct.product)
            ]
        )

    async def get_products_with_buy_flag(
            self,
            basket_id: int,
            buy_in_next_order: bool = True
    ) -> Basket | None:
        query = (
            select(Basket)
            .options(
                selectinload(Basket.product_on_basket)
                .selectinload(BasketProduct.product),
                with_loader_criteria(
                    BasketProduct,
                    BasketProduct.buy_in_next_order == buy_in_next_order
                )
            )
            .where(Basket.basket_id == basket_id)
        )
        return await self.session.scalar(query)