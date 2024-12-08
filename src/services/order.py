import uuid
from typing import Annotated

from fastapi import Depends

from exceptions.product import ProductNotInStock, ProductQuantityException
from models.basket import BasketProduct
from models.order import Order
from unitofworks.order_uow import OrderBasketWork


class OrderService:
    def __init__(self, uow: Annotated[OrderBasketWork, Depends(OrderBasketWork)]):
        self.uow = uow

    async def create(self, user_id: str | uuid.UUID, products: list[BasketProduct]):
        async with self.uow:
            price = 0
            order = await self.uow.order_repository.create(user_id=user_id, order_price=price)
            for one_product in products:
                if not one_product.product.in_stock:
                    raise ProductNotInStock(one_product.product.name)
                if one_product.product_count > one_product.product.quantity:
                    raise ProductQuantityException(one_product.product.name)
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

    async def get_one(self, order_id: int) -> Order | None:
        async with self.uow:
            order = await self.uow.order_repository.get(order_id)
            return order

    async def get_all(self, user_id: str | uuid.UUID) -> list[Order]:
        async with self.uow:
            orders = await self.uow.order_repository.get_all(user_id)
            return orders
