import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get(self, user_id: uuid.UUID) -> User | None:
        return await self.session.get(User, user_id)