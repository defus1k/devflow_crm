from aiogram import Router, types, F
from sqlalchemy import select, func, and_

from app.db.session import async_session
from app.models.order import Order

router = Router()


@router.callback_query(F.data == "manager_stats")
async def show_statistics(callback: types.CallbackQuery):
    async with async_session() as session:
        created_total = await session.scalar(select(func.count(Order.id)).where(Order.manager_id == callback.from_user.id)) or 0
        active_total = await session.scalar(select(func.count(Order.id)).where(and_(Order.manager_id == callback.from_user.id, Order.status.in_(["in_progress", "pending"])))) or 0
        completed_total = await session.scalar(select(func.count(Order.id)).where(and_(Order.manager_id == callback.from_user.id, Order.status == "completed"))) or 0
        revenue_total = await session.scalar(select(func.coalesce(func.sum(Order.budget), 0)).where(and_(Order.manager_id == callback.from_user.id, Order.status == "completed"))) or 0

    success_percent = round((completed_total / created_total * 100), 1) if created_total else 0.0
    text = (
        f"📊 Моя статистика\n\n"
        f"Создано заявок: {created_total}\n"
        f"Активные заказы: {active_total}\n"
        f"Завершённые заказы: {completed_total}\n"
        f"Процент успешно завершённых проектов: {success_percent}%\n"
        f"Общий доход: {float(revenue_total):.2f}"
    )
    await callback.message.answer(text)
    await callback.answer()