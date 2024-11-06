import uuid

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column

from db import Base, async_session


class UserRole(Base):
    __tablename__ = 'role'
    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str]

    @classmethod
    async def create_default_roles(cls):
        async with async_session() as session:
            if await session.scalar(select(UserRole)) is None:
                session.add_all([
                    UserRole(role_id=1, role_name="Администратор"),
                    UserRole(role_id=2, role_name="Пользователь")
                ])
                await session.commit()


class User(Base):
    __tablename__ = 'user'
    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    firstname: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    user_role: Mapped[int] = mapped_column(ForeignKey(UserRole.role_id))

