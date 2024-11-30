import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from models.basket import Basket


class BasketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create(self, user_id: uuid.UUID | str):
        basket = Basket(user_id=user_id)
        self.session.add(basket)