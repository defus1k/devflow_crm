from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    
    position: Mapped[str] = mapped_column(String(50))
    topic: Mapped[str] = mapped_column(String(100), nullable=False) 

    applicant_name: Mapped[str] = mapped_column(String(255))
    age: Mapped[str] = mapped_column(String(50))
    experience: Mapped[str] = mapped_column(String(255))
    skills: Mapped[str] = mapped_column(Text)
    portfolio: Mapped[str] = mapped_column(Text)
    motivation: Mapped[str] = mapped_column(Text)
    online: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(30), default="pending")
    
    # ДОБАВЬТЕ ЭТУ СТРОКУ, чтобы убрать ошибку NOT NULL
    message: Mapped[str] = mapped_column(Text, nullable=True) 

    user = relationship("User", backref="worker_applications")