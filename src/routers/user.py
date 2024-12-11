import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.user import current_user, validate_update_user, current_admin_user
from schemas.response import ResponseModel, UserResponse
from schemas.user import UserPayload, UpdateUserSchema, AdminUpdateUserSchema
from services.user import UserServices

user_router = APIRouter(prefix='/user', tags=["User"])


@user_router.get("")
async def get_info_about_user(
        user_payload: Annotated[UserPayload, Depends(current_user)],
        user_service: Annotated[UserServices, Depends(UserServices)]
):
    user = await user_service.get_info_attrs(user_payload.user_id)
    return UserResponse(detail="Ваши данные", data=user)


@user_router.patch("")
async def edit_user(
        update_user_schema: Annotated[UpdateUserSchema, Depends(validate_update_user)],
        user: Annotated[UserPayload, Depends(current_user)],
        user_service: Annotated[UserServices, Depends(UserServices)]
):
    await user_service.update(user.user_id, update_user_schema)
    return ResponseModel(detail="Данные были успешно обновлены!")


@user_router.patch("/admin/{user_id}", dependencies=[Depends(current_admin_user)])
async def edit_user_role(
        user_id: uuid.UUID,
        update_user_schema: AdminUpdateUserSchema,
        user_service: Annotated[UserServices, Depends(UserServices)]
):
    await user_service.update(user_id, update_user_schema)
    return ResponseModel(detail="Данные были успешно обновлены!")
