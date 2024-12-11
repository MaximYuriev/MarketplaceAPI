import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.user import User, UserRole


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_id: uuid.UUID | str) -> User | None:
        user = await self.session.get(User, user_id, options=[selectinload(User.basket)])
        return user

    async def get_user_by_params(self, **kwargs) -> User | None:
        query = select(User).options(selectinload(User.basket)).filter_by(**kwargs)
        user = await self.session.scalar(query)
        return user

    async def get_info_attrs(self, user_id: uuid.UUID | str):
        query = (
            select(User.firstname, User.surname, User.email, UserRole.role_name)
            .join(UserRole, User.user_role == UserRole.role_id)
            .where(User.user_id == user_id)
        )
        user = await self.session.execute(query)
        return user.first()

    async def create(self, user_data: dict) -> uuid.UUID:
        user = User(**user_data)
        self.session.add(user)
        await self.session.flush()
        return user.user_id

    def update(self, user: User, user_data: dict):
        for key, value in user_data.items():
            setattr(user, key, value)
