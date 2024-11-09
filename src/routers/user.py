from fastapi import APIRouter, Depends, Response
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.jwt import create_access_token, create_refresh_token
from db import get_session
from dependencies.user import validate_user, current_user, current_admin_user
from models.token import RefreshToken
from models.user import User
from schemas.user import UserCreate, UserPayload
from auth import utils
from settings import COOKIE_KEY


user_router = APIRouter(prefix='/user', tags=["User"])


@user_router.post("/reg")
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    user_create.password = utils.hash_password(user_create.password)
    data = user_create.model_dump()
    user = User(**data)
    session.add(user)
    await session.commit()


@user_router.post("/login")
async def auth_user(response:Response,
                    user:User = Depends(validate_user), session:AsyncSession = Depends(get_session)):
    access_token = create_access_token(user)
    token = await session.scalar(select(RefreshToken).where(RefreshToken.user_id == user.user_id))
    if token is None:
        refresh_token = create_refresh_token(user)
        token = RefreshToken(refresh_token=refresh_token, user_id=user.user_id)
        session.add(token)
        await session.commit()
    else:
        try:
            utils.decode_jwt(token.refresh_token)
        except InvalidTokenError:
            await session.delete(token)
            refresh_token = create_refresh_token(user)
            token = RefreshToken(refresh_token=refresh_token, user_id=user.user_id)
            session.add(token)
            await session.commit()
    response.set_cookie(COOKIE_KEY, access_token)
    return {"detail": "Пользователь успешно авторизован!"}


@user_router.get("/info")
def get_info_about_user(user:UserPayload = Depends(current_user)):
    return {"detail": f"Hello, {user.name}"}

@user_router.get("/private_info")
def get_private_info(user: UserPayload = Depends(current_admin_user)):
    return {"detail": f"Hello, {user.name} you are admin! graz!"}

