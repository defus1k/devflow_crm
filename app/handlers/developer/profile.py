from aiogram import Router, types
from aiogram.filters import Command
from app.db.session import async_session
from app.models.user import User
from sqlalchemy import select

router = Router()

@router.message(Command("dev_profile"))
async def show_dev_profile(message: types.Message):
    async with async_session() as session:
        result = await session.execute(
            select(User).filter(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
    
    if not user:
        await message.answer("Профіль не знайдено.")
        return

    profile_text = (
        f"👤 **Профіль розробника**\n\n"
        f"Ім'я: {user.full_name}\n"
        f"ID: {user.telegram_id}\n"
        f"Ранг/Роль: {user.role}\n\n"
        "💡 *Для зміни контактних даних або навичок зверніться до менеджера.*"
    )
    
    await message.answer(profile_text, parse_mode="Markdown")