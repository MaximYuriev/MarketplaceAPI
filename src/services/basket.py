from typing import Annotated

from fastapi import Depends

from models.basket import Basket
from repositories.basket import BasketRepository


class BasketService:
    def __init__(self, repository: Annotated[BasketRepository, Depends(BasketRepository)]):
        self.repository = repository

    async def get_all_products(self, basket_id: int) -> Basket | None:
        return await self.repository.get_products(basket_id)

    async def get_all_products_with_buy_flag(
            self,
            basket_id: int,
            buy_in_next_order: bool = True
    ) -> Basket | None:
        return await self.repository.get_products_with_buy_flag(basket_id, buy_in_next_order)
