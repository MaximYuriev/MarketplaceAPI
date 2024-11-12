from fastapi import Depends, HTTPException, status

from auth.jwt import JWT
from models.user import User
from repositories.access_token import AccessTokenRepository
from schemas.token import AccessTokenPayload


class AccessTokenServices:
    def __init__(self, token_repository: AccessTokenRepository = Depends()):
        self.repository = token_repository

    def create_token(self, user: User):
        access_token_payload = AccessTokenPayload.model_validate(user, from_attributes=True)
        token = JWT.create_jwt(access_token_payload)
        self.repository.create(token)

    def get_token(self):
        token = self.repository.get()
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не авторизован!"
            )
        return token

    def delete_token(self):
        return self.repository.delete()