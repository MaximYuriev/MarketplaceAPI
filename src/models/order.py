import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class OrderProduct(Base):
    __tablename__ = "order_product"
    order_id: Mapped[int] = mapped_column(ForeignKey("order.order_id", ondelete="CASCADE"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id", ondelete="CASCADE"), primary_key=True)


class Order(Base):
    __tablename__ = "order"
    order_id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int]
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow())

    products: Mapped[list["Product"]] = relationship(secondary="order_product")
