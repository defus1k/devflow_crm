from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.user import User
from sqlalchemy import select

router = Router()

@router.message(Command("notifications"))
async def setup_notifications(message: types.Message):
    """
    Виводить меню налаштувань сповіщень.
    """
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()

    builder = InlineKeyboardBuilder()
    
    # Визначаємо поточний стан (true/false)
    status_emoji = "✅" if user.notifications_enabled else "❌"
    
    builder.button(
        text=f"Сповіщення: {status_emoji}", 
        callback_data="toggle_notifications"
    )
    
    await message.answer(
        "⚙️ **Налаштування сповіщень**\n\n"
        "Керуйте отриманням повідомлень про ваші замовлення:",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == "toggle_notifications")
async def toggle_notifications(callback: types.CallbackQuery):
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.telegram_id == callback.from_user.id))
        user = result.scalar_one_or_none()
        
        # Перемикаємо стан
        user.notifications_enabled = not user.notifications_enabled
        await session.commit()
    
    new_status = "Увімкнено" if user.notifications_enabled else "Вимкнено"
    await callback.answer(f"Сповіщення {new_status}")
    
    # Оновлюємо клавіатуру
    await setup_notifications(callback.message)