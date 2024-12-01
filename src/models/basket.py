import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Basket(Base):
    __tablename__ = "basket"
    basket_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.user_id"))

class BasketProduct(Base):
    __tablename__ = "basket_product"
    basket_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id"), primary_key=True)
    product_count: Mapped[int] = mapped_column(default=1)

