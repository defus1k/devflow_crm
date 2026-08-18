from datetime import datetime

from sqlalchemy import (
    BigInteger,
    String,
    ForeignKey,
    Integer,
    DateTime,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Кто оставил отзыв
    user_id: Mapped[int] = mapped_column(BigInteger)

    user_name: Mapped[str] = mapped_column(String(255))

    # Если отзыв относится к заказу
    order_id: Mapped[int | None] = mapped_column(
        ForeignKey("orders.id"),
        nullable=True,
    )

    # Оценка
    rating: Mapped[int] = mapped_column(Integer)

    # Текст
    text: Mapped[str] = mapped_column(String(1000))

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    order = relationship("Order", backref="reviews")

    def __repr__(self):
        return f"<Review {self.id}>"