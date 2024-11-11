from typing import Annotated

from fastapi import APIRouter, Depends, Response, HTTPException
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.jwt import JWT
from db import get_session
from dependencies.user import validate_user, current_user, current_admin_user, current_user_for_refresh
from models.user import User
from schemas.user import UserCreate, UserPayload
from auth import utils
from services.access_token import AccessTokenServices
from services.refresh_token import RefreshTokenServices
from services.user import UserServices

user_router = APIRouter(prefix='/user', tags=["User"])


@user_router.post("/reg")
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    user_create.password = utils.hash_password(user_create.password)
    data = user_create.model_dump()
    user = User(**data)
    session.add(user)
    await session.commit()


@user_router.post("/login")
async def auth_user(
        user:Annotated[User, Depends(validate_user)],
        refresh_token_services: RefreshTokenServices = Depends(),
        access_token_services: AccessTokenServices = Depends()
):
    access_token_services.create_token(user)
    try:
        refresh_token = await refresh_token_services.get_token(user.user_id)
    except HTTPException:
        await refresh_token_services.create_token(user)
    else:
        try:
            JWT.parse_jwt(refresh_token.refresh_token)
        except InvalidTokenError:
            await refresh_token_services.delete_token(refresh_token)
            await refresh_token_services.create_token(user)
    return {"detail": "Пользователь успешно авторизован!"}


@user_router.get("/info")
def get_info_about_user(user:UserPayload = Depends(current_user)):
    return {"detail": f"Hello, {user.name}"}

@user_router.get("/private_info")
def get_private_info(user: UserPayload = Depends(current_admin_user)):
    return {"detail": f"Hello, {user.name} you are admin! graz!"}

@user_router.post("/refresh")
async def refresh_access_token(
        payload: UserPayload = Depends(current_user_for_refresh),
        user_services: UserServices = Depends(),
        access_token_services: AccessTokenServices = Depends(),
        refresh_token_services: RefreshTokenServices = Depends()
):
    token = await refresh_token_services.get_token(payload.user_id)
    try:
        refresh_token_payload = JWT.parse_jwt(token.refresh_token)
    except InvalidTokenError:
        await refresh_token_services.delete_token(token)
        access_token_services.delete_token()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен!"
        )
    if refresh_token_payload.get("sub") != payload.user_id:
        await refresh_token_services.delete_token(token)
        access_token_services.delete_token()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен!"
        )
    user = await user_services.get_user_by_id(payload.user_id)
    print(user)
    return access_token_services.create_token(user)