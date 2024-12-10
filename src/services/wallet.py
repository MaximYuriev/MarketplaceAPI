import uuid
from typing import Annotated

from fastapi import Depends

from models.wallet import Wallet
from repositories.wallet import WalletRepository
from schemas.balance import UpdateBalanceSchema


class WalletService:
    def __init__(self, repository: Annotated[WalletRepository, Depends(WalletRepository)]):
        self.repository = repository

    async def get(self, user_id: uuid.UUID | str) -> Wallet | None:
        return await self.repository.get(user_id)

    async def update(self, wallet: Wallet, update_balance: UpdateBalanceSchema) -> Wallet:
        update_data = update_balance.model_dump()
        update_data["balance"] = wallet.balance + update_data["balance"]
        wallet = await self.repository.update(wallet, update_data)
        return wallet