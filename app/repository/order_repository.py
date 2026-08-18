from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.models.order import Order, OrderStatus

class OrderRepository:
    """
    Репозиторій для управління замовленнями.
    Використовує Eager Loading (joinedload) для отримання даних користувачів.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, client_id: int, title: str, description: str, budget: float) -> Order:
        """Створення нового замовлення."""
        order = Order(
            client_id=client_id,
            title=title,
            description=description,
            budget=budget
        )
        self.session.add(order)
        await self.session.flush()
        return order

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        """Отримання детальної інформації про замовлення разом з учасниками."""
        result = await self.session.execute(
            select(Order)
            .options(joinedload(Order.client), joinedload(Order.manager), joinedload(Order.developer))
            .where(Order.id == order_id)
        )
        return result.unique().scalar_one_or_none()

    async def get_by_status(self, status: OrderStatus) -> List[Order]:
        """Пошук усіх замовлень за певним статусом."""
        result = await self.session.execute(
            select(Order).where(Order.status == status)
        )
        return list(result.scalars().all())

    async def update_status(self, order_id: int, new_status: OrderStatus) -> bool:
        """Оновлення статусу замовлення."""
        result = await self.session.execute(
            update(Order)
            .where(Order.id == order_id)
            .values(status=new_status)
        )
        return result.rowcount > 0

    async def assign_staff(self, order_id: int, manager_id: Optional[int] = None, developer_id: Optional[int] = None) -> bool:
        """Призначення відповідальних осіб на замовлення."""
        values = {}
        if manager_id: values["manager_id"] = manager_id
        if developer_id: values["developer_id"] = developer_id
        
        result = await self.session.execute(
            update(Order)
            .where(Order.id == order_id)
            .values(**values)
        )
        return result.rowcount > 0