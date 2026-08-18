from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.payment import Payment # Ми створимо цю модель наступною
from app.models.order import Order
from sqlalchemy import select, func # Добавьте func
class PaymentRepository:
    """
    Репозиторій для керування фінансовими транзакціями.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment(self, order_id: int, amount: float, provider: str, status: str = "pending") -> Payment:
        """Реєстрація нової транзакції."""
        payment = Payment(
            order_id=order_id,
            amount=amount,
            provider=provider,
            status=status
        )
        self.session.add(payment)
        await self.session.flush()
        return payment

    async def get_order_payments(self, order_id: int) -> List[Payment]:
        """Отримання списку всіх платежів по конкретному замовленню."""
        result = await self.session.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        return list(result.scalars().all())

    async def update_payment_status(self, payment_id: int, status: str) -> bool:
        """Оновлення статусу транзакції (наприклад, після підтвердження від CryptoBot)."""
        payment = await self.session.get(Payment, payment_id)
        if payment:
            payment.status = status
            return True
        return False

    async def get_total_revenue(self) -> float:
        """Підрахунок загального доходу системи (приклад агрегації)."""
        # Спрощений приклад агрегації даних
        result = await self.session.execute(
            select(func.sum(Payment.amount)).where(Payment.status == "completed")
        )
        return result.scalar() or 0.0