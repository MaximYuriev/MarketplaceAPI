from typing import Annotated

from fastapi import APIRouter, Depends
from jwt import InvalidTokenError

from auth.jwt import JWT
from dependencies.refresh_token import current_user_from_refresh_token
from dependencies.user import validate_user, validate_email_unique
from exceptions.token import TokenNotFound
from models.user import User
from schemas.response import ResponseModel
from schemas.user import UserCreate
from services.access_token import AccessTokenServices
from services.refresh_token import RefreshTokenServices
from services.user import UserServices

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/reg")
async def registration(
        user_create: Annotated[UserCreate, Depends(validate_email_unique)],
        user_services: UserServices = Depends()
):
    await user_services.create_user(user_create)
    return ResponseModel(detail="Пользователь успешной зарегистрирован!")

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
    return ResponseModel(detail="Пользователь вошел в аккаунт!")

@auth_router.get("/refresh")
async def refresh_access_token(
        user: User = Depends(current_user_from_refresh_token),
        access_token_services: AccessTokenServices = Depends()
):
    access_token_services.create_token(user)
    return ResponseModel(detail="Токен обновлен!")