from sqlalchemy import BigInteger, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Кому відправлено
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    
    # Тип сповіщення (наприклад: "order_status", "reminder", "promo")
    type: Mapped[str] = mapped_column(String(50))
    
    # Текст повідомлення
    content: Mapped[str] = mapped_column(Text)
    
    # Статус: "sent", "failed", "pending"
    status: Mapped[str] = mapped_column(String(20), default="pending")
    
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    
    # Зв'язок
    user = relationship("User", backref="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.type}, status={self.status})>"