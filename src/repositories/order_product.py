from sqlalchemy.ext.asyncio import AsyncSession

from models.order import OrderProduct


class OrderProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create(self, **kwargs):
        order_product = OrderProduct(**kwargs)
        self.session.add(order_product)