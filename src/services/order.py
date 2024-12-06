from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import with_config
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from exceptions.product import ProductNotInStock, ProductQuantityException
from models.order import Order, OrderProduct
from unitofworks.order_uow import OrderBasketWork


class OrderService:
    def __init__(self, uow: Annotated[OrderBasketWork, Depends(OrderBasketWork)]):
        self.uow = uow

    async def create(self, basket_id: int):
        async with self.uow:
            products_on_basket = await self.uow.basket_product_repository.get_all_by_params(basket_id=basket_id)
            if not products_on_basket:
                raise HTTPException(status_code=404, detail="Корзина пуста!")
            amount = 0
            order = await self.uow.order_repository.create(amount=0)
            for one_product in products_on_basket:
                if not one_product.product.in_stock:
                    raise ProductNotInStock
                if one_product.product_count > one_product.product.quantity:
                    raise ProductQuantityException
                amount += one_product.product.price * one_product.product_count
                one_product.product.quantity -= one_product.product_count
                if one_product.product.quantity == 0:
                    one_product.product.in_stock = False
                self.uow.order_product_repository.create(order_id=order.order_id, product_id=one_product.product_id)
                await self.uow.session.delete(one_product)
            order.amount = amount
            await self.uow.commit()

    async def get(self, order_id: int) -> Order | None:
        async with self.uow:
            order = await self.uow.order_repository.get(order_id)
            self.uow.session.expunge_all()
            return order