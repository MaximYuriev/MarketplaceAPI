import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Wallet(Base):
    __tablename__ = "wallet"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True)
    balance: Mapped[int] = mapped_column(default=0)