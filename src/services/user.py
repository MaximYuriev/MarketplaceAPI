import uuid

from fastapi import HTTPException, status, Depends

from repositories.user import UserRepository


class UserServices:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.repository = user_repository

    async def get_user_by_id(self, user_id: uuid.UUID | str):
        user = await self.repository.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден!"
            )
        return user