from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from repositories.basket import BasketRepository
from repositories.user import UserRepository


class UserBasketWork:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    async def __aenter__(self):
        self.user_repository = UserRepository(self.session)
        self.basket_repository = BasketRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
