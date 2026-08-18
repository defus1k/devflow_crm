from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.order import Order
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta

router = Router()

@router.callback_query(F.data == "manage_reports")
async def show_reports(callback: types.CallbackQuery):
    """
    Формує звіт за останні 30 днів.
    """
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    async with async_session() as session:
        # Кількість завершених замовлень
        completed_count = await session.scalar(
            select(func.count(Order.id)).where(
                and_(Order.status == "completed", Order.updated_at >= thirty_days_ago)
            )
        )
        
        # Загальний обіг коштів
        total_revenue = await session.scalar(
            select(func.sum(Order.budget)).where(
                and_(Order.status == "completed", Order.updated_at >= thirty_days_ago)
            )
        ) or 0

    report_text = (
        "📈 **Звіт за останні 30 днів**\n\n"
        f"✅ Виконано замовлень: {completed_count}\n"
        f"💰 Загальний обіг: {total_revenue} USD\n"
        "--------------------------\n"
        "Використовуйте /dashboard для повернення до управління."
    )
    
    await callback.message.edit_text(report_text, parse_mode="Markdown")
    await callback.answer()