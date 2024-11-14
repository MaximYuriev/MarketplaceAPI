import uuid

from fastapi.params import Depends

from auth.config import EXPIRE_TOKEN_DAYS
from auth.jwt import JWT
from exceptions.token import TokenNotFound
from models.token import RefreshToken
from models.user import User
from repositories.refresh_token import RefreshTokenRepository
from schemas.token import RefreshTokenPayload


class RefreshTokenServices:
    def __init__(
            self,
            refresh_token_repository: RefreshTokenRepository = Depends(),
    ):
        self.refresh_repository = refresh_token_repository

    async def get_token(self, user_id: uuid.UUID | str):
        token = await self.refresh_repository.get(user_id)
        if token is None:
            raise TokenNotFound
        return token

    async def create_token(self, user: User):
        refresh_token_payload = RefreshTokenPayload.model_validate(user, from_attributes=True)
        refresh_token = JWT.create_jwt(refresh_token_payload, expire_timedelta=EXPIRE_TOKEN_DAYS)
        token = RefreshToken(refresh_token=refresh_token, user_id=user.user_id)
        await self.refresh_repository.create(token)

    async def delete_token(self, token: RefreshToken):
        await self.refresh_repository.delete(token)