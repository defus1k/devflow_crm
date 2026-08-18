from sqlalchemy import BigInteger, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Balance(Base):
    __tablename__ = "balances"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"), primary_key=True)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0.00)
    
    # Використовуємо back_populates замість backref для уникнення конфліктів
    user = relationship("User", back_populates="balance_record", uselist=False)

    def __repr__(self):
        return f"<Balance(user={self.user_id}, amount={self.amount})>"