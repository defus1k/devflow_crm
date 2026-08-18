from sqlalchemy import String, Text, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Warning(Base):
    __tablename__ = "warnings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Кому винесено попередження
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    
    # Хто виніс попередження (можна залишити nullable, якщо це система)
    admin_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"), nullable=True)
    
    # Причина попередження
    reason: Mapped[str] = mapped_column(String(255))
    
    # Деталі (наприклад, посилання на повідомлення з порушенням)
    details: Mapped[str] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Зв'язок
    user = relationship("User", foreign_keys=[user_id], backref="warnings")

    def __repr__(self):
        return f"<Warning(id={self.id}, user={self.user_id}, reason={self.reason})>"