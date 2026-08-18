from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from app.db.session import async_session
from app.models.user import User
from sqlalchemy import select

router = Router()
OWNER_ID = 1268981313 # Ваш ID

class BroadcastState(StatesGroup):
    waiting_for_text = State()

# 1. Запуск команди
@router.message(Command("broadcast"))
async def start_broadcast(message: Message, state: FSMContext):
    if message.from_user.id != OWNER_ID:
        return
    await message.answer("📣 Введіть текст для розсилки:")
    await state.set_state(BroadcastState.waiting_for_text)

# 2. Отримання тексту та розсилка
@router.message(BroadcastState.waiting_for_text)
async def process_broadcast(message: Message, state: FSMContext, bot: Bot):
    async with async_session() as session:
        # Отримуємо всі ID користувачів
        users = await session.execute(select(User.telegram_id))
        user_ids = users.scalars().all()

    await message.answer(f"⏳ Починаю розсилку на {len(user_ids)} користувачів...")
    
    count = 0
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, message.text)
            count += 1
        except Exception:
            continue
            
    await message.answer(f"✅ Готово! Повідомлення отримали {count} користувачів.")
    await state.clear()