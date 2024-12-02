import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_id: uuid.UUID | str) -> User | None:
        return await self.session.get(User, user_id, options=[selectinload(User.basket)])

    async def get_user_by_params(self, **kwargs):
        query = select(User).options(selectinload(User.basket)).filter_by(**kwargs)
        return await self.session.scalar(query)

    async def create(self, user_data: dict) -> uuid.UUID:
        user = User(**user_data)
        self.session.add(user)
        await self.session.flush()
        return user.user_id

    async def update(self, user: User, user_data: dict):
        for key, value in user_data.items():
            setattr(user, key, value)
