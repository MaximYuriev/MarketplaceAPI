import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from .user import User


class Product(Base):
    __tablename__ = 'product'
    product_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(User.user_id))
    in_stock: Mapped[bool] = mapped_column(default=True)

    added_by: Mapped["User"] = relationship()

    def __repr__(self):
        return f'{self.product_id}'