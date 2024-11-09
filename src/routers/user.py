from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from models.token import RefreshToken
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

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

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
        expire_minutes=1
    )

def create_refresh_token(user:User) -> str:
    jwt_payload = {"sub": str(user.user_id)}
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=30)
    )

@user_router.post("/login")
async def auth_user(response:Response,
                    user:User = Depends(validate_user), session:AsyncSession = Depends(get_session)):
    access_token = create_access_token(user)
    token = await session.scalar(select(RefreshToken).where(RefreshToken.user_id == user.user_id))
    if token is None:
        refresh_token = create_refresh_token(user)
        token = RefreshToken(refresh_token=refresh_token, user_id=user.user_id)
        session.add(token)
    else:
        try:
            utils.decode_jwt(token)
        except InvalidTokenError:
            await session.delete(token)
            refresh_token = create_refresh_token(user)
            token = RefreshToken(refresh_token=refresh_token, user_id=user.user_id)
            session.add(token)
    await session.commit()
    response.set_cookie(COOKIE_KEY, access_token)
    return {"detail": "Пользователь успешно авторизован!"}

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
            detail=f"Неверный тип токена: {token_type!r}! Ожидаемый тип - {ACCESS_TOKEN_TYPE!r}"
        )
    return UserPayload.model_validate(payload, from_attributes=True)

def current_admin_user(payload: dict = Depends(current_token_payload), user_exist: bool = Depends(check_user_exist)):
    if payload.get("role") == 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа!"
        )
    return UserPayload.model_validate(payload, from_attributes=True)

@user_router.get("/info")
def get_info_about_user(user:UserPayload = Depends(current_user)):
    return {"detail": f"Hello, {user.name}"}

@user_router.get("/private_info")
def get_private_info(user: UserPayload = Depends(current_admin_user)):
    return {"detail": f"Hello, {user.name} you are admin! graz!"}

