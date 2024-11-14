from fastapi import Depends

from auth import utils
from auth.config import ACCESS_TOKEN_TYPE
from dependencies.token import current_token_payload, current_token_payload_for_refresh
from exceptions.token import TokenTypeException, TokenInvalidException
from exceptions.user import UserAccessException, UserValidateError, UserEmailNotUnique
from schemas.user import UserLogin, UserPayload, UserCreate
from services.user import UserServices


async def validate_user(user_login: UserLogin, user_services: UserServices = Depends()):
    user = await user_services.get_user_by_email(user_login.email)
    if user is not None:
        if utils.validate_password(user_login.password, user.password):
            return user
    raise UserValidateError

async def validate_email_unique(user_create: UserCreate, user_services: UserServices = Depends()):
    if await user_services.get_user_by_email(user_create.email):
        raise UserEmailNotUnique
    return user_create

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