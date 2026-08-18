from sqlalchemy import BigInteger, String, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Withdrawal(Base):
    __tablename__ = "withdrawals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Хто отримує кошти або ініціює вивід
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    
    # Сума виведення
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    
    # Спосіб виведення (наприклад, "card", "crypto", "cash")
    method: Mapped[str] = mapped_column(String(50))
    
    # Статус: pending, approved, rejected
    status: Mapped[str] = mapped_column(String(50), default="pending")
    
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    
    # Зв'язок
    user = relationship("User", backref="withdrawals")

    def __repr__(self):
        return f"<Withdrawal(id={self.id}, amount={self.amount}, status={self.status})>"