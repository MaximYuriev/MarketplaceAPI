from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.wallet import current_user_wallet
from models.wallet import Wallet
from schemas.balance import UpdateBalanceSchema
from schemas.response import ResponseModel, BalanceResponse
from services.wallet import WalletService

wallet_router = APIRouter(prefix="/wallet", tags=["Wallet"])


@wallet_router.get("")
async def view_balance(
        wallet: Annotated[Wallet, Depends(current_user_wallet)]
):
    return BalanceResponse(detail="Ваш баланс:", data=wallet)


@wallet_router.patch("")
async def top_up_balance(
        update_balance: UpdateBalanceSchema,
        wallet: Annotated[Wallet, Depends(current_user_wallet)],
        wallet_service: Annotated[WalletService, Depends(WalletService)]
):
    updated_wallet = await wallet_service.update(wallet, update_balance)
    return BalanceResponse(detail="Баланс успешно изменен!", data=updated_wallet)
