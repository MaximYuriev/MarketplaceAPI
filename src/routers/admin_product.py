from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.product import current_product
from dependencies.user import current_admin_user
from models.product import Product
from schemas.product import ProductSchema, ProductUpdate
from schemas.response import ResponseProductModel, ResponseModel
from schemas.user import UserPayload
from services.product import ProductServices

admin_product_router = APIRouter(
    prefix="/admin_panel/product",
    tags=['ProductAdminPanel'],
    dependencies=[Depends(current_admin_user)]
)

@admin_product_router.post("/add")
async def add_new_product(
        product: ProductSchema,
        admin: UserPayload = Depends(current_admin_user),
        product_services: ProductServices = Depends()
):
    product = await product_services.create(product, admin.user_id)
    return ResponseProductModel(
        detail="Товар создан!",
        data=ProductSchema.model_validate(product, from_attributes=True)
    )

@admin_product_router.patch("/{product_id}")
async def update_product(
        product: Annotated[Product, Depends(current_product)],
        product_update: ProductUpdate,
        product_services: ProductServices = Depends()
):
    changed_product = await product_services.update(product, product_update)
    return ResponseProductModel(
        detail="Товар обновлен!",
        data=ProductSchema.model_validate(changed_product, from_attributes=True)
    )

@admin_product_router.delete("/{product_id}")
async def delete_product(
        product: Annotated[Product,Depends(current_product)],
        product_services: ProductServices = Depends()
):
    await product_services.delete(product)
    return ResponseModel(detail="Товар удален")
