from typing import Annotated

from fastapi import Depends

from dependencies.product import current_product
from dependencies.user import current_user
from exceptions.basket import BasketIsEmpty
from exceptions.product import ProductNotInStock, ProductQuantityException, ProductNotInBasket
from models.basket import BasketProduct
from models.product import Product
from schemas.basket import AddProductOnBasketSchema, UpdateProductOnBasketSchema
from schemas.user import UserPayload
from services.basket_product import BasketProductService
from services.product import ProductServices


async def current_added_product(
        added_product_data: AddProductOnBasketSchema,
        product_service: ProductServices = Depends(),

) -> Product:
    product = await current_product(added_product_data.product_id, product_service)
    return product


async def product_on_basket(
        product: Annotated[Product, Depends(current_product)],
        user: Annotated[UserPayload, Depends(current_user)],
        basket_product_service: Annotated[BasketProductService, Depends(BasketProductService)]
) -> BasketProduct:
    basket_product = await basket_product_service.get_one(basket_id=user.basket_id, product_id=product.product_id)
    if basket_product is None:
        raise ProductNotInBasket
    return basket_product


async def products_on_basket(
        user: Annotated[UserPayload, Depends(current_user)],
        basket_product_service: Annotated[BasketProductService, Depends(BasketProductService)],
) -> list[BasketProduct]:
    basket = await basket_product_service.get_all_products_with_buy_flag(basket_id=user.basket_id, buy_in_next_order=True)
    if basket is None or not basket.product_on_basket:
        raise BasketIsEmpty
    return basket.product_on_basket


async def validate_add_product_on_basket(
        added_product_data: AddProductOnBasketSchema,
        product: Annotated[Product, Depends(current_added_product)]
) -> AddProductOnBasketSchema:
    if not product.in_stock:
        raise ProductNotInStock(product.name)

    if added_product_data.product_count > product.quantity:
        raise ProductQuantityException(product.name)

    return added_product_data


async def validate_update_product_on_basket(
        updated_product_data: UpdateProductOnBasketSchema,
        product: Annotated[Product, Depends(current_product)],
) -> UpdateProductOnBasketSchema:
    if updated_product_data.product_count is not None and updated_product_data.product_count > product.quantity:
        raise ProductQuantityException(product.name)

    return updated_product_data
