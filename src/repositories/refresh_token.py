import uuid

from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from models.token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create(self, token: RefreshToken):
        self.session.add(token)
        await self.session.commit()

    async def get(self, user_id: uuid.UUID | str) -> RefreshToken | None:
        return await self.session.scalar(select(RefreshToken).where(RefreshToken.user_id == user_id))

    async def delete(self, token: RefreshToken):
        await self.session.delete(token)
        await self.session.commit()