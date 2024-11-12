from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from auth import utils
from auth.jwt import JWT
from db import get_session
from dependencies.refresh_token import current_user_from_refresh_token
from dependencies.user import validate_user
from exceptions.exception import TokenInvalidException, TokenNotFound
from models.user import User
from schemas.user import UserCreate
from services.access_token import AccessTokenServices
from services.refresh_token import RefreshTokenServices

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/reg")
async def registration(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    user_create.password = utils.hash_password(user_create.password)
    data = user_create.model_dump()
    user = User(**data)
    session.add(user)
    await session.commit()

@auth_router.post("/login")
async def login(
        user:Annotated[User, Depends(validate_user)],
        refresh_token_services: RefreshTokenServices = Depends(),
        access_token_services: AccessTokenServices = Depends()
):
    access_token_services.create_token(user)
    try:
        refresh_token = await refresh_token_services.get_token(user.user_id)
    except TokenNotFound:
        await refresh_token_services.create_token(user)
    else:
        try:
            JWT.parse_jwt(refresh_token.refresh_token)
        except InvalidTokenError:
            await refresh_token_services.delete_token(refresh_token)
            await refresh_token_services.create_token(user)
    return {"detail": "Пользователь успешно авторизован!"}

@auth_router.post("/refresh")
async def refresh_access_token(
        user: User = Depends(current_user_from_refresh_token),
        access_token_services: AccessTokenServices = Depends()
):
    return access_token_services.create_token(user)