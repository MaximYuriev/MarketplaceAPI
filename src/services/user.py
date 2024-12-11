import uuid
from typing import Annotated

from fastapi import Depends
from pydantic import EmailStr

from auth import utils
from exceptions.user import UserNotFound
from models.user import User
from schemas.user import UserCreate, UpdateUserSchema, AdminUpdateUserSchema
from unitofworks.user_basket_work import UserBasketWork


class UserServices:
    def __init__(self, uow: Annotated[UserBasketWork, Depends(UserBasketWork)]):
        self.uow = uow

    async def create_user(self, user_create: UserCreate):
        user_create.password = utils.hash_password(user_create.password)
        user_data = user_create.model_dump()
        async with self.uow:
            user_id = await self.uow.user_repository.create(user_data)
            self.uow.basket_repository.create(user_id)
            self.uow.wallet_repository.create(user_id)
            await self.uow.commit()

    async def get_user_by_id(self, user_id: uuid.UUID | str) -> User:
        async with self.uow:
            user = await self.uow.user_repository.get(user_id)
            if user is None:
                raise UserNotFound
            self.uow.session.expunge_all()
            return user

    async def get_info_attrs(self, user_id: uuid.UUID | str):
        async with self.uow:
            user = await self.uow.user_repository.get_info_attrs(user_id)
            return user

    async def get_user_by_email(self, email: EmailStr | str):
        async with self.uow:
            user = await self.uow.user_repository.get_user_by_params(email=email)
            self.uow.session.expunge_all()
            return user

    async def update(self, user_id: uuid.UUID | str, update_user: UpdateUserSchema | AdminUpdateUserSchema):
        update_data = update_user.model_dump(exclude_none=True)
        async with self.uow:
            user = await self.uow.user_repository.get(user_id)
            if user is None:
                raise UserNotFound
            self.uow.user_repository.update(user, update_data)
            await self.uow.commit()
