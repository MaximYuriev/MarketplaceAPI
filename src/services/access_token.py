from fastapi import Depends

from auth.jwt import JWT
from exceptions.user import UserNotAuthorized
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
            raise UserNotAuthorized
        return token

    def delete_token(self):
        return self.repository.delete()