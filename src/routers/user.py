from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from models.user import User
from schemas.user import UserCreate, UserLogin, UserPayload
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


async def validate_user(user_login: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await session.scalar(select(User).where(User.email == user_login.email))
    if user is not None:
        if utils.validate_password(user_login.password, user.password):
            return user
    raise HTTPException(400, "bad request")

@user_router.post("/login")
async def auth_user(response:Response,
                    user:User = Depends(validate_user)):
    jwt_payload = {
        "sub": str(user.user_id),
        "email":user.email,
        "name":f"{user.firstname} {user.surname}",
        "role":user.user_role
    }
    token = utils.encode_jwt(jwt_payload)
    response.set_cookie(COOKIE_KEY, token)
    return {"detail": "Пользователь успешно авторизован!"}

def current_token_payload(request: Request):
    token = request.cookies.get(COOKIE_KEY)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован!"
        )
    try:
        return utils.decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен!"
        )

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
    return UserPayload.model_validate(payload, from_attributes=True)

def current_admin_user(payload: dict = Depends(current_token_payload), user_exist: bool = Depends(check_user_exist)):
    if payload.get("role") == 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа!"
        )
    return UserPayload.model_validate(payload, from_attributes=True)

@user_router.get("/info")
async def get_info_about_user(user:UserPayload = Depends(current_user)):
    return {"detail": f"Hello, {user.name}"}

@user_router.get("/private_info")
async def get_private_info(user: UserPayload = Depends(current_admin_user)):
    return {"detail": f"Hello, {user.name} you are admin! graz!"}