from aiogram import Router, types
from aiogram.filters import Command
from app.db.session import async_session
from app.models.user import User
from sqlalchemy import select

# Імпортуйте всі ваші функції клавіатур
from app.keyboards.client import get_client_kb
from app.keyboards.manager import get_manager_kb
from app.keyboards.owner.dashboard import get_owner_dashboard_kb

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    async with async_session() as session:
        # ЗАВЖДИ беремо свіжі дані з БД
        user = await session.scalar(select(User).where(User.telegram_id == message.from_user.id))
        
        if not user:
            await message.answer("Ви не зареєстровані в системі.")
            return

        # ВИБІР МЕНЮ В ЗАЛЕЖНОСТІ ВІД РОЛІ
        if user.role == "owner":
            # Тут можна додати виклик функції, що порахує дані для кнопок
            await message.answer("👑 Вітаємо, Власнику!", reply_markup=get_owner_dashboard_kb(0, 0, 0))
        elif user.role == "manager":
            await message.answer("💼 Панель менеджера:", reply_markup=get_manager_kb())
        else:
            await message.answer("👤 Ваш кабінет:", reply_markup=get_client_kb())