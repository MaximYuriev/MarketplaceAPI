from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError

from dependencies.basket import validate_add_product_on_basket, product_on_basket, validate_update_product_on_basket
from dependencies.user import current_user
from exceptions.product import ProductAlreadyInBasket
from models.basket import BasketProduct
from schemas.basket import AddProductOnBasketSchema, UpdateProductOnBasketSchema
from schemas.response import ResponseModel, BasketResponse
from schemas.user import UserPayload
from services.basket_product import BasketProductService

basket_router = APIRouter(prefix="/basket", tags=["Basket"], dependencies=[Depends(current_user)])


@basket_router.post("")
async def add_product_on_basket(
        product: Annotated[AddProductOnBasketSchema, Depends(validate_add_product_on_basket)],
        user: Annotated[UserPayload, Depends(current_user)],
        basket_product_service: Annotated[BasketProductService, Depends(BasketProductService)]
):
    try:
        await basket_product_service.add_product(user.basket_id, product)
        return ResponseModel(detail="Товар успешно добавлен в корзину!")
    except IntegrityError:
        raise ProductAlreadyInBasket


@basket_router.get("")
async def get_all_product_on_basket(
        basket_product_service: Annotated[BasketProductService, Depends(BasketProductService)],
        user: Annotated[UserPayload, Depends(current_user)]
):
    basket = await basket_product_service.get_all_products(user.basket_id)
    return BasketResponse(detail="Ваша корзина", data=basket)


@basket_router.put("/{product_id}")
async def update_product_on_basket(
        product: Annotated[UpdateProductOnBasketSchema, Depends(validate_update_product_on_basket)],
        basket_product: Annotated[BasketProduct, Depends(product_on_basket)],
        basket_product_service: Annotated[BasketProductService, Depends(BasketProductService)]
):
    await basket_product_service.update(basket_product, product)
    return ResponseModel(detail="Товар в корзине успешно изменен!")


@basket_router.delete("/{product_id}")
async def delete_product_on_basket(
        basket_product: Annotated[BasketProduct, Depends(product_on_basket)],
        basket_product_service: Annotated[BasketProductService, Depends(BasketProductService)]
):
    await basket_product_service.delete(basket_product)
    return ResponseModel(detail="Товар успешно удален!")
