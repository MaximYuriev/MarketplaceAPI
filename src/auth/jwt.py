from datetime import timedelta

from fastapi import HTTPException, Depends
from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from auth import utils
from auth.config import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from db import get_session
from models.token import RefreshToken
from models.user import User
from schemas.user import UserPayload
from settings import COOKIE_KEY


def create_jwt(token_type: str, token_data: dict, expire_minutes: int = 15, expire_timedelta: timedelta | None = None) -> str:
    jwt_payload = {"type":token_type}
    jwt_payload.update(token_data)
    return utils.encode_jwt(jwt_payload, expire_minutes=expire_minutes, expire_timedelta=expire_timedelta)


def create_access_token(user:User) -> str:
    jwt_payload = {
        "sub": str(user.user_id),
        "email": user.email,
        "name": f"{user.firstname} {user.surname}",
        "role": user.user_role
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=15
    )


def create_refresh_token(user:User) -> str:
    jwt_payload = {"sub": str(user.user_id)}
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=30)
    )


async def refresh_access_token(payload: UserPayload, session: AsyncSession, response: Response):
    token = await session.scalar(select(RefreshToken).where(RefreshToken.user_id == payload.user_id))
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован!"
        )
    try:
        refresh_token_payload = utils.decode_jwt(token.refresh_token)
    except InvalidTokenError:
        await session.delete(token)
        await session.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен!"
        )
    if refresh_token_payload.get("sub") != payload.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен!"
        )
    user = await session.get(User, payload.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден!"
        )
    access_token = create_access_token(user)
    response.set_cookie(COOKIE_KEY, access_token)
    return access_token


async def current_token_payload(response: Response, request: Request, session: AsyncSession = Depends(get_session)):
    token = request.cookies.get(COOKIE_KEY)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован!"
        )
    try:
        return utils.decode_jwt(token)
    except ExpiredSignatureError:
        expired_token_payload = utils.decode_jwt(token, verify_signature=False)
        payload = UserPayload.model_validate(expired_token_payload, from_attributes=True)
        new_token = await refresh_access_token(payload, session, response)
        return utils.decode_jwt(new_token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен!"
        )
