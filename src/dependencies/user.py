from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth import utils
from auth.config import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE
from db import get_session
from models.user import User
from auth.jwt import current_token_payload
from schemas.user import UserLogin, UserPayload


async def validate_user(user_login: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await session.scalar(select(User).where(User.email == user_login.email))
    if user is not None:
        if utils.validate_password(user_login.password, user.password):
            return user
    raise HTTPException(400, "bad request")


async def check_user_exist(payload: dict = Depends(current_token_payload),
                           session: AsyncSession = Depends(get_session)):
    user_id = payload.get("sub")
    if await session.get(User, user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен",
        )
    return True


def current_user(payload: dict = Depends(current_token_payload), user_exist: bool = Depends(check_user_exist)):
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != ACCESS_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Неверный тип токена: {token_type!r}! Ожидаемый тип - {ACCESS_TOKEN_TYPE !r}"
        )
    return UserPayload.model_validate(payload, from_attributes=True)


def current_admin_user(payload: dict = Depends(current_token_payload), user_exist: bool = Depends(check_user_exist)):
    if payload.get("role") == 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа!"
        )
    return UserPayload.model_validate(payload, from_attributes=True)
