import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get(self, user_id: uuid.UUID | str) -> User | None:
        return await self.session.get(User, user_id)

    async def get_user_by_params(self, **kwargs):
        query = select(User).filter_by(**kwargs)
        return await self.session.scalar(query)

    async def create(self, user_data: dict):
        user = User(**user_data)
        self.session.add(user)
        await self.session.commit()

    async def update(self, user: User, user_data: dict):
        for key, value in user_data.items():
            setattr(user, key, value)
        await self.session.commit()