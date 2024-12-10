import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from models.wallet import Wallet


class WalletRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    def create(self, user_id: uuid.UUID | str):
        wallet = Wallet(user_id=user_id)
        self.session.add(wallet)

    async def get(self, user_id: uuid.UUID | str) -> Wallet | None:
        return await self.session.get(Wallet, user_id)

    async def update(self, wallet: Wallet, update_data: dict) -> Wallet:
        for key, value in update_data.items():
            setattr(wallet, key, value)
        await self.session.commit()
        return wallet
