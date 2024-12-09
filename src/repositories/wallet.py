import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from models.wallet import Wallet


class WalletRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create(self, user_id: uuid.UUID | str):
        wallet = Wallet(user_id=user_id)
        self.session.add(wallet)