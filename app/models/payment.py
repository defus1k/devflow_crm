from sqlalchemy import BigInteger, String, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Зв'язок із замовленням
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    
    # Сума транзакції
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    
    # Статус платежу: pending, success, failed, refunded
    status: Mapped[str] = mapped_column(String(50), default="pending")
    
    # ID транзакції у зовнішній системі (наприклад, Stripe Charge ID або Monobank Invoice ID)
    provider_payment_id: Mapped[str] = mapped_column(String(255), nullable=True)
    
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    
    # Зв'язок для зручного доступу: payment.order.user
    order = relationship("Order", backref="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount}, status={self.status})>"