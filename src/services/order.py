import uuid
from typing import Annotated

from fastapi import Depends, HTTPException

from exceptions.product import ProductNotInStock, ProductQuantityException
from models.order import Order
from unitofworks.order_uow import OrderBasketWork


class OrderService:
    def __init__(self, uow: Annotated[OrderBasketWork, Depends(OrderBasketWork)]):
        self.uow = uow

    async def create(self, user_id: str | uuid.UUID, basket_id: int):
        async with self.uow:
            products_on_basket = await self.uow.basket_product_repository.get_all_by_params(basket_id=basket_id)
            if not products_on_basket:
                raise HTTPException(status_code=404, detail="Корзина пуста!")
            price = 0
            order = await self.uow.order_repository.create(user_id=user_id, order_price=0)
            for one_product in products_on_basket:
                if not one_product.product.in_stock:
                    raise ProductNotInStock
                if one_product.product_count > one_product.product.quantity:
                    raise ProductQuantityException
                product_on_order_price = one_product.product.price * one_product.product_count
                price += product_on_order_price
                one_product.product.quantity -= one_product.product_count
                if one_product.product.quantity == 0:
                    one_product.product.in_stock = False
                self.uow.order_product_repository.create(
                    order_id=order.order_id,
                    product_id=one_product.product_id,
                    product_count=one_product.product_count,
                    product_on_order_price=product_on_order_price
                )
                await self.uow.session.delete(one_product)
            order.order_price = price
            await self.uow.commit()

    async def get(self, order_id: int) -> Order | None:
        async with self.uow:
            order = await self.uow.order_repository.get(order_id)
            self.uow.session.expunge_all()
            return order