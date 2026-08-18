from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.db.session import async_session
from app.models.user import User
from sqlalchemy import select

router = Router()

# Ваш ID власника (ви можете додати сюди інші ID, якщо потрібно)
ALLOWED_IDS = [1268981313] 

class AdminBroadcast(StatesGroup):
    waiting_for_text = State()

# --- ОБРОБКА РОЗСИЛКИ ЧЕРЕЗ АДМІН-ПАНЕЛЬ ---
@router.callback_query(F.data == "admin_broadcast")
async def ask_broadcast_text(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("📣 Введіть текст технічного сповіщення для користувачів:")
    await state.set_state(AdminBroadcast.waiting_for_text)
    await callback.answer()

# --- КОМАНДА ДЛЯ ВЛАСНИКА (ОКРЕМО) ---
@router.message(Command("broadcast"))
async def owner_broadcast_command(message: types.Message, state: FSMContext):
    if message.from_user.id not in ALLOWED_IDS:
        return
    await message.answer("📣 Введіть текст глобальної розсилки для всіх користувачів:")
    await state.set_state(AdminBroadcast.waiting_for_text)

# --- СПІЛЬНА ЛОГІКА РОЗСИЛКИ ---
@router.message(AdminBroadcast.waiting_for_text)
async def send_technical_broadcast(message: types.Message, state: FSMContext, bot: Bot):
    async with async_session() as session:
        # Отримуємо всіх користувачів
        users = await session.execute(select(User.telegram_id))
        user_ids = users.scalars().all()

    await message.answer(f"⏳ Починаю розсилку на {len(user_ids)} користувачів...")
    
    success_count = 0
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, f"📢 **Глобальне повідомлення:**\n\n{message.text}")
            success_count += 1
        except Exception:
            continue
            
    await message.answer(f"✅ Розсилка завершена. Отримали: {success_count} користувачів.")
    await state.clear()