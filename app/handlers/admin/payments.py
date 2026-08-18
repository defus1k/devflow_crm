from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from app.core.config import settings # імпорт твоїх налаштувань

router = Router()

@router.callback_query(F.data.startswith("add_"))
async def admin_add_money(callback: CallbackQuery, bot: Bot):
    _, user_id, order_id, amount = callback.data.split("_")
    
    # --- СЮДИ ВСТАВ СВІЙ КОД БД ДЛЯ ПОПОВНЕННЯ ---
    
    await bot.send_message(int(user_id), f"✅ Баланс поповнено на {amount} грн!")
    await callback.message.edit_text(
        text=f"{callback.message.text}\n\n✅ <b>Зараховано: {amount} грн</b>\n👤 <b>Адмін:</b> {callback.from_user.full_name}",
        parse_mode="HTML"
    )
    
    # Сповіщення менеджеру
    await bot.send_message(
        chat_id=settings.MANAGER_FORUM_ID,
        text=f"🚀 <b>Оплата підтверджена!</b>\nЗамовлення: #{order_id}\nСума: {amount} грн",
        parse_mode="HTML"
    )
    
    await callback.answer("Готово!")

@router.callback_query(F.data.startswith("reject_"))
async def admin_reject(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f"{callback.message.text}\n\n❌ <b>Відхилено: {callback.from_user.full_name}</b>",
        parse_mode="HTML"
    )
    await callback.answer("Відхилено")