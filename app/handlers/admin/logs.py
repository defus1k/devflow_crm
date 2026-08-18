from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.log import SystemLog
from sqlalchemy import select

router = Router()

# 1. Головна кнопка "📜 Логи" (Reply)
@router.message(F.text == "📜 Логи")
async def show_logs_menu(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Переглянути останні 20 подій", callback_data="admin_logs_list")
    builder.adjust(1)
    
    await message.answer(
        "📜 <b>Система логування:</b>\nОберіть дію для перегляду технічних даних:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

# 2. Відкриття меню логів з панелі (Inline)
@router.callback_query(F.data == "admin_logs_menu")
async def open_logs_menu_from_panel(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Переглянути останні 20 подій", callback_data="admin_logs_list")
    builder.adjust(1)

    await callback.message.edit_text(
        "📜 <b>Система логування:</b>\nОберіть дію для перегляду технічних даних:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()

# 3. Список останніх логів (Inline)
@router.callback_query(F.data == "admin_logs_list")
async def list_logs_inline(callback: types.CallbackQuery):
    async with async_session() as session:
        # Отримуємо останні 20 записів
        query = select(SystemLog).order_by(SystemLog.created_at.desc()).limit(20)
        result = await session.execute(query)
        logs = result.scalars().all()
    
    if not logs:
        return await callback.answer("📜 Журнал подій порожній.")
    
    log_text = "📜 <b>Останні події:</b>\n\n"
    for log in logs:
        time_str = log.created_at.strftime('%H:%M') if log.created_at else "--:--"
        action = (log.action or "system").replace("moderation_", "")
        details = log.details or "Без деталей"
        label = "модерація" if log.action and log.action.startswith("moderation_") else "система"
        log_text += f"• <code>{time_str}</code> | <b>{label}</b> | {action}: {details}\n"
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Оновити", callback_data="admin_logs_list")
    builder.button(text="🔙 Назад", callback_data="logs_back")
    builder.adjust(1)
    
    await callback.message.edit_text(log_text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

# 4. Кнопка "Назад"
@router.callback_query(F.data == "logs_back")
async def back_to_logs_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📜 <b>Система логування:</b>\nОберіть дію для перегляду технічних даних:",
        reply_markup=InlineKeyboardBuilder().button(text="📝 Переглянути останні 20 подій", callback_data="admin_logs_list").as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()