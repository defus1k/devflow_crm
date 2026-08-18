from sqlalchemy import BigInteger, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class SystemLog(Base):
    __tablename__ = "system_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Хто здійснив дію (якщо це користувач)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"), nullable=True)
    
    # Яка подія відбулася (наприклад: "order_status_change", "withdrawal_request")
    action: Mapped[str] = mapped_column(String(100))
    
    # Опис змін (наприклад: "Статус замовлення #5 змінено з pending на paid")
    details: Mapped[str] = mapped_column(Text)
    
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<SystemLog(id={self.id}, action={self.action})>"