from typing import Annotated

from fastapi import APIRouter, Depends

from cache.cache import cache
from dependencies.product import current_product, product_query_parameters, validate_create_product, \
    validate_update_product
from dependencies.user import current_admin_user
from models.product import Product
from schemas.product import ProductSchema, ProductUpdate
from schemas.response import ResponseProductModel, ResponseModel
from schemas.user import UserPayload
from services.product import ProductServices

product_router = APIRouter(
    prefix="/product",
    tags=['Product'],
)


@product_router.post("/add", dependencies=[Depends(current_admin_user)])
async def add_new_product(
        product: Annotated[ProductSchema, Depends(validate_create_product)],
        admin: Annotated[UserPayload, Depends(current_admin_user)],
        product_services: Annotated[ProductServices, Depends(ProductServices)]
):
    product = await product_services.create(product, admin.user_id)
    return ResponseProductModel(
        detail="Товар добавлен!",
        data=product
    )


@product_router.patch("/{product_id}", dependencies=[Depends(current_admin_user)])
async def update_product(
        product: Annotated[Product, Depends(current_product)],
        product_update: Annotated[ProductUpdate, Depends(validate_update_product)],
        product_services: Annotated[ProductServices, Depends(ProductServices)]
):
    changed_product = await product_services.update(product, product_update)
    return ResponseProductModel(
        detail="Товар обновлен!",
        data=changed_product
    )


@product_router.delete("/{product_id}", dependencies=[Depends(current_admin_user)])
async def delete_product(
        product: Annotated[Product, Depends(current_product)],
        product_services: Annotated[ProductServices, Depends(ProductServices)]
):
    await product_services.delete(product)
    return ResponseModel(detail="Товар удален")


@product_router.get("/{product_id}")
@cache(expire=60)
async def get_product(
        product: Annotated[Product, Depends(current_product)],
):
    return ResponseProductModel(
        detail="Товар найден!",
        data=product
    )


@product_router.get("")
@cache(expire=60)
async def get_all_products(
        product_service: Annotated[ProductServices, Depends(ProductServices)],
        query_parameters: Annotated[dict, Depends(product_query_parameters)]
):
    products = await product_service.get_all_products(**query_parameters)
    return ResponseProductModel(
        detail="Все товары",
        data=products
    )
