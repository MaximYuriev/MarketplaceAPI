import uuid

from fastapi import HTTPException, status, Response, Request
from fastapi.params import Depends

from auth.config import EXPIRE_TOKEN_DAYS
from auth.jwt import JWT
from models.token import RefreshToken
from models.user import User
from repositories.access_token import AccessTokenRepository
from repositories.refresh_token import RefreshTokenRepository
from schemas.token import RefreshTokenPayload


class RefreshTokenServices:
    def __init__(
            self,
            refresh_token_repository: RefreshTokenRepository = Depends(),
            access_token_repository: AccessTokenRepository = Depends()
    ):
        self.refresh_repository = refresh_token_repository
        self.access_repository = access_token_repository

    async def get_token(self, user_id: uuid.UUID | str):
        token = await self.refresh_repository.get(user_id)
        if token is None:
            self.access_repository.delete()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не авторизован!",
                headers=self.access_repository.response.headers
            )
        return token

    async def create_token(self, user: User):
        refresh_token_payload = RefreshTokenPayload.model_validate(user, from_attributes=True)
        refresh_token = JWT.create_jwt(refresh_token_payload, expire_timedelta=EXPIRE_TOKEN_DAYS)
        token = RefreshToken(refresh_token=refresh_token, user_id=user.user_id)
        await self.refresh_repository.create(token)

    async def delete_token(self, token: RefreshToken):
        await self.refresh_repository.delete(token)