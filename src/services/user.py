import uuid

from fastapi import Depends

from auth import utils
from exceptions.user import UserNotFound
from models.user import User
from repositories.user import UserRepository
from schemas.user import UserCreate


class UserServices:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.repository = user_repository

    async def create_user(self, user_create: UserCreate):
        user_create.password = utils.hash_password(user_create.password)
        user_data = user_create.model_dump()
        await self.repository.create(user_data)

    async def get_user_by_id(self, user_id: uuid.UUID | str) -> User:
        user = await self.repository.get(user_id)
        if user is None:
            raise UserNotFound
        return user

    async def get_user_by_email(self, email: str):
        return await self.repository.get_user_by_params(email=email)