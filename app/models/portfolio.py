from sqlalchemy import String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Portfolio(Base):
    __tablename__ = "portfolio"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Назва проекту або кейсу
    title: Mapped[str] = mapped_column(String(255))
    
    # Детальний опис кейсу
    description: Mapped[str] = mapped_column(Text)
    
    # Посилання на проект або фото/відео доказ
    link: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Опціонально: прив'язка до менеджера, який виконав цей кейс
    manager_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"), nullable=True)
    
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Зв'язок
    manager = relationship("User", backref="portfolio_items")

    def __repr__(self):
        return f"<Portfolio(title={self.title})>"