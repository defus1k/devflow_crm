from sqlalchemy import String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Автор запиту
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    
    # Тема та опис
    subject: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    
    # Статус: open, in_progress, resolved, closed
    status: Mapped[str] = mapped_column(String(50), default="open")
    
    # Пріоритет: low, medium, high
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, onupdate=func.now())

    # Зв'язок
    user = relationship("User", backref="tickets")

    def __repr__(self):
        return f"<Ticket(id={self.id}, subject={self.subject}, status={self.status})>"