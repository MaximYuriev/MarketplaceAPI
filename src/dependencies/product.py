from typing import Annotated

from fastapi import Depends

from exceptions.product import ProductAlreadyExist, ProductNameNotUnique, ProductNotFound
from schemas.product import ProductSchema, ProductUpdate
from services.product import ProductServices


async def current_product(
        product_id: int,
        product_services: ProductServices = Depends()
):
    product = await product_services.get(product_id=product_id)
    if product is None:
        raise ProductNotFound
    return product


async def validate_create_product(
        product: ProductSchema,
        product_service: Annotated[ProductServices, Depends(ProductServices)]
):
    if await product_service.get(name=product.name):
        raise ProductAlreadyExist
    return product


async def validate_update_product(
        product: ProductUpdate,
        product_service: Annotated[ProductServices, Depends(ProductServices)]
):
    if product.name is not None:
        if await product_service.get(name=product.name):
            raise ProductNameNotUnique
    return product


def product_query_parameters(
        name: str | None = None,
        in_stock: bool | None = None,
        price: int | None = None,
        description: str | None = None
):
    return query_parameters(name=name, in_stock=in_stock, price=price, description=description)


def query_parameters(**kwargs):
    query_params = {}
    for key, value in kwargs.items():
        if kwargs[key] is not None:
            query_params[key] = value
    return query_params
