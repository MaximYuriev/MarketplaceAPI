from typing import Annotated

from fastapi import Depends

from auth import utils
from auth.config import ACCESS_TOKEN_TYPE
from dependencies.token import current_token_payload, current_token_payload_for_refresh
from exceptions.token import TokenTypeException, TokenInvalidException
from exceptions.user import UserAccessException, UserValidateError, UserEmailNotUnique
from schemas.user import UserLogin, UserPayload, UserCreate, UpdateUserSchema
from services.user import UserServices


async def validate_email(
        user: UserCreate | UpdateUserSchema,
        user_service: UserServices
) -> UserCreate | UpdateUserSchema:
    if await user_service.get_user_by_email(user.email):
        raise UserEmailNotUnique
    return user


async def validate_user(user_login: UserLogin, user_services: UserServices = Depends()):
    user = await user_services.get_user_by_email(user_login.email)
    if user is not None:
        if utils.validate_password(user_login.password, user.password):
            return user
    raise UserValidateError


async def validate_email_unique(user_create: UserCreate, user_services: UserServices = Depends()):
    return await validate_email(user_create, user_services)


async def validate_update_user(
        user_update: UpdateUserSchema,
        user_service: Annotated[UserServices, Depends(UserServices)]
) -> UpdateUserSchema:
    if user_update.email:
        return await validate_email(user_update, user_service)
    return user_update


async def check_user_exist(payload: dict = Depends(current_token_payload),
                           user_services: UserServices = Depends()):
    user_id = payload.get("sub")
    if await user_services.get_user_by_id(user_id) is None:
        raise TokenInvalidException
    return True


def current_user(payload: dict = Depends(current_token_payload), user_exist: bool = Depends(check_user_exist)):
    token_type = payload.get('type')
    if token_type != ACCESS_TOKEN_TYPE:
        raise TokenTypeException
    return UserPayload.model_validate(payload, from_attributes=True)


def current_admin_user(payload: dict = Depends(current_token_payload), user_exist: bool = Depends(check_user_exist)):
    if payload.get("role") == 2:
        raise UserAccessException
    return UserPayload.model_validate(payload, from_attributes=True)


def current_user_for_refresh(payload: dict = Depends(current_token_payload_for_refresh)):
    token_type = payload.get('type')
    if token_type != ACCESS_TOKEN_TYPE:
        raise TokenTypeException
    return UserPayload.model_validate(payload, from_attributes=True)
