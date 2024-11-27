import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import Base
from .user import User


class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    refresh_token: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(User.user_id))