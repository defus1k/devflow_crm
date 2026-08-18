from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.models.user import User


class DeveloperService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order_scope(self, developer_id: int, status: str | None = None) -> list[Order]:
        query = select(Order).where(Order.developer_id == developer_id)
        if status:
            query = query.where(Order.status == status)
        result = await self.session.execute(query.order_by(Order.created_at.desc()))
        return list(result.scalars().all())

    async def get_project_stats(self, developer_id: int) -> dict[str, Any]:
        completed = await self.session.scalar(
            select(func.count(Order.id)).where(and_(Order.developer_id == developer_id, Order.status == "completed"))
        ) or 0
        in_progress = await self.session.scalar(
            select(func.count(Order.id)).where(and_(Order.developer_id == developer_id, Order.status == "in_progress"))
        ) or 0
        under_review = await self.session.scalar(
            select(func.count(Order.id)).where(and_(Order.developer_id == developer_id, Order.status == "under_review"))
        ) or 0
        total_income = await self.session.scalar(
            select(func.coalesce(func.sum(Order.budget), 0)).where(and_(Order.developer_id == developer_id, Order.status == "completed"))
        ) or 0
        return {
            "completed": int(completed),
            "in_progress": int(in_progress),
            "under_review": int(under_review),
            "total_income": float(total_income),
        }

    async def get_developer(self, developer_id: int) -> User | None:
        return await self.session.get(User, developer_id)

    async def update_order_status(self, order: Order, status: str) -> None:
        order.status = status
        order.updated_at = datetime.utcnow()

    async def update_progress(self, order: Order, progress: int) -> None:
        order.description = f"{order.description}\n[progress:{progress}%]"
        order.updated_at = datetime.utcnow()

    async def update_deadline(self, order: Order, deadline: datetime) -> None:
        order.description = f"{order.description}\n[deadline:{deadline.strftime('%Y-%m-%d')}]"
        order.updated_at = datetime.utcnow()

    async def add_issue_note(self, order: Order, note: str) -> None:
        order.description = f"{order.description}\n[issue:{note}]"
        order.updated_at = datetime.utcnow()

    async def can_access_order(self, developer_id: int, order: Order) -> bool:
        return order.developer_id == developer_id or order.manager_id == developer_id
