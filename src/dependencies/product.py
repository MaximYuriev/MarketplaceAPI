from fastapi import Depends

from services.product import ProductServices


async def current_product(product_id: int, product_services: ProductServices = Depends()):
    return await product_services.get(product_id)