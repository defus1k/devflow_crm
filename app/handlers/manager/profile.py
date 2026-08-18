from aiogram import Router, types
from aiogram.filters import Command
from app.db.session import async_session
from app.models.user import User
from sqlalchemy import select

router = Router()

@router.message(Command("manager_profile"))
async def show_manager_profile(message: types.Message):
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.telegram_id == message.from_user.id))
        manager = result.scalar_one_or_none()
    
    if not manager:
        await message.answer("Профіль менеджера не знайдено.")
        return

    profile_text = (
        f"👔 **Профіль Менеджера**\n\n"
        f"Ім'я: {manager.full_name}\n"
        f"ID: {manager.telegram_id}\n"
        f"Рівень доступу: {manager.role}\n\n"
        f"Активних проєктів під контролем: 5\n" # Можна додати динамічний підрахунок
        "--------------------------\n"
        "Для редагування даних зверніться до адміністратора."
    )
    
    await message.answer(profile_text, parse_mode="Markdown")