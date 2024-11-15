from fastapi import APIRouter, Depends

from dependencies.user import current_admin_user
from schemas.product import ProductSchema
from schemas.response import ResponseProductModel
from schemas.user import UserPayload
from services.product import ProductServices

product_router = APIRouter(prefix="/product", tags=['Product'])

@product_router.post("/add")
async def add_new_product(
        product: ProductSchema,
        admin: UserPayload = Depends(current_admin_user),
        product_services: ProductServices = Depends()
):
    product = await product_services.create(product, admin.user_id)
    return ResponseProductModel(
        detail="Продукт создан!",
        data=ProductSchema.model_validate(product, from_attributes=True)
    )