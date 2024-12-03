import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class BasketProduct(Base):
    __tablename__ = "basket_product"
    basket_id: Mapped[int] = mapped_column(ForeignKey("basket.basket_id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id"), primary_key=True)
    product_count: Mapped[int] = mapped_column(default=1)

    product: Mapped["Product"] = relationship()


class Basket(Base):
    __tablename__ = "basket"
    basket_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.user_id"))

    product_on_basket: Mapped[list["BasketProduct"]] = relationship()
