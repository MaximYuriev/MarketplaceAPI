from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.user import current_user
from schemas.order import OuterOrderSchema
from schemas.response import ResponseModel, OrderResponse
from schemas.user import UserPayload
from services.order import OrderService

order_router = APIRouter(prefix="/order", tags=["Order"])


@order_router.get("/{order_id}", dependencies=[Depends(current_user)])
async def get_order_info(
        order_id: int,
        order_service: Annotated[OrderService, Depends(OrderService)]
):
    order = await order_service.get_one(order_id)
    return OrderResponse(detail="Найденный заказ:", data=order)


@order_router.get("")
async def get_all_orders_info(
        user: Annotated[UserPayload, Depends(current_user)],
        order_service: Annotated[OrderService, Depends(OrderService)]
):
    orders = await order_service.get_all(user.user_id)
    return OrderResponse(detail="История заказов", data=orders)


@order_router.post("")
async def make_order(
        user: Annotated[UserPayload, Depends(current_user)],
        order_service: Annotated[OrderService, Depends(OrderService)]
):
    await order_service.create(user.user_id, user.basket_id)
    return ResponseModel(detail="Заказ успешно сформирован!")
