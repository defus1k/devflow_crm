from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select, and_

from app.db.session import async_session
from app.models.order import Order

router = Router()


@router.callback_query(F.data == "manager_salary")
async def show_salary_pending(callback: types.CallbackQuery):
    async with async_session() as session:
        query = select(Order).where(and_(Order.manager_id == callback.from_user.id, Order.status == "completed"))
        result = await session.execute(query)
        completed_orders = result.scalars().all()

    total_income = sum(float(order.budget or 0) for order in completed_orders)
    text = (
        f"💰 Мои заработки\n\n"
        f"Начисления: {len(completed_orders)} завершённых заказов\n"
        f"Выплаты: 0\n"
        f"Общий доход: {total_income:.2f}"
    )
    await callback.message.answer(text)
    await callback.answer()