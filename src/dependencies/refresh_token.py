from fastapi import Depends
from jwt import InvalidTokenError

from auth.jwt import JWT
from dependencies.user import current_user_for_refresh
from exceptions.exception import TokenInvalidException
from models.token import RefreshToken
from schemas.user import UserPayload
from services.refresh_token import RefreshTokenServices
from services.user import UserServices


async def get_token_from_payload(
    user_payload: UserPayload = Depends(current_user_for_refresh),
    refresh_token_services: RefreshTokenServices = Depends()
):
    return await refresh_token_services.get_token(user_payload.user_id)

async def parse_refresh_token(
        token: RefreshToken = Depends(get_token_from_payload),
        refresh_token_services: RefreshTokenServices = Depends()
):
    try:
       return JWT.parse_jwt(token.refresh_token)
    except InvalidTokenError:
        await refresh_token_services.delete_token(token)
        raise TokenInvalidException

async def current_user_from_refresh_token(
        refresh_token_payload: dict = Depends(parse_refresh_token),
        user_services: UserServices = Depends()
):
    user_id = refresh_token_payload.get("sub")
    if user_id is None:
        raise TokenInvalidException
    return await user_services.get_user_by_id(user_id)