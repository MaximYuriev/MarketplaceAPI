from typing import Annotated

from fastapi import Depends

from dependencies.user import current_user
from models.wallet import Wallet
from schemas.user import UserPayload
from services.wallet import WalletService


async def current_user_wallet(
        user: Annotated[UserPayload, Depends(current_user)],
        wallet_service: Annotated[WalletService, Depends(WalletService)]
) -> Wallet | None:
    return await wallet_service.get(user.user_id)
