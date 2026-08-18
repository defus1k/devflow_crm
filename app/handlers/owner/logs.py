from aiogram import Router, types, F
from app.db.session import async_session
from app.models.log import SystemLog # Припустима модель логів
from sqlalchemy import select

router = Router()

@router.callback_query(F.data == "owner_logs")
async def show_system_logs(callback: types.CallbackQuery):
    async with async_session() as session:
        # Витягуємо останні 20 подій
        result = await session.execute(
            select(SystemLog).order_by(SystemLog.created_at.desc()).limit(20)
        )
        logs = result.scalars().all()

    if not logs:
        await callback.message.edit_text("📜 Журнал подій порожній.")
        return

    log_text = "📜 **Останні системні події:**\n\n"
    for log in logs:
        log_text += f"[{log.created_at.strftime('%H:%M')}] {log.event_type}: {log.description}\n"

    await callback.message.edit_text(log_text[:4096]) # Обмеження Telegram
    await callback.answer()