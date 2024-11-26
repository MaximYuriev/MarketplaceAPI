from fastapi import Depends

from services.product import ProductServices


async def current_product(product_id: int, product_services: ProductServices = Depends()):
    return await product_services.get(product_id)


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
