import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.order import Order, OrderProduct


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Order:
        order = Order(**kwargs)
        self.session.add(order)
        await self.session.flush()
        return order

    def update(self, order: Order, update_order: dict):
        for key, value in update_order.items():
            setattr(order, key, value)

    async def get(self, order_id: int) -> Order | None:
        query = (
            select(Order)
            .options(selectinload(Order.products).selectinload(OrderProduct.product))
            .where(Order.order_id == order_id)
        )
        return await self.session.scalar(query)

    async def get_all(self, user_id: str | uuid.UUID) -> Sequence[Order]:
       query = (
           select(Order)
           .options(selectinload(Order.products).selectinload(OrderProduct.product))
           .where(Order.user_id == user_id)
           .order_by(Order.created_at.desc())
       )
       result = await self.session.scalars(query)
       return result.all()