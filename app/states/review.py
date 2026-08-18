from sqlalchemy import ForeignKey, String, Text, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Review(Base):
    """
    Модель відгуку клієнта про виконане замовлення.
    """
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), unique=True, nullable=False)
    
    # Оцінка від 1 до 5
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Зв'язки
    order = relationship("Order", backref="review", uselist=False)

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

    def __repr__(self) -> str:
        return f"<Review(id={self.id}, rating={self.rating})>"