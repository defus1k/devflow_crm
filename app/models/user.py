from decimal import Decimal
from enum import StrEnum
from sqlalchemy import BigInteger, String, DateTime, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class UserRole(StrEnum):
    CLIENT = "client"
    MANAGER = "manager"
    DEVELOPER = "developer"
    ADMIN = "admin"
    OWNER = "owner"


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), nullable=True)
    full_name: Mapped[str] = mapped_column(String(128))
    role: Mapped[str] = mapped_column(String(20), default=UserRole.CLIENT)
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00")) 
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Зв'язки
    balance_record = relationship("Balance", back_populates="user", uselist=False)
    # ПОВНИЙ ШЛЯХ до моделі модерації
    moderation = relationship("app.models.moderation.UserModeration", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.telegram_id}, role={self.role}, balance={self.balance})>"