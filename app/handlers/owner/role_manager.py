from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from app.db.session import async_session
from app.models.user import User
from sqlalchemy import select
import logging

router = Router()
MY_TELEGRAM_ID = 1268981313

@router.message(Command("whois"))
async def get_user_info(message: types.Message, command: CommandObject):
    if message.from_user.id != MY_TELEGRAM_ID:
        return

    if not command.args:
        await message.answer("❌ Використання: /whois @username")
        return

    username = command.args.lstrip('@')
    
    try:
        async with async_session() as session:
            # Використовуємо запит без зайвих ризиків
            stmt = select(User).where(User.username == username)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if user:
                info = (
                    f"👤 <b>Профіль:</b> {user.full_name}\n"
                    f"🆔 ID: <code>{user.telegram_id}</code>\n"
                    f"🏷 Юзернейм: @{user.username}\n"
                    f"🛡 Роль: <code>{user.role}</code>"
                )
                await message.answer(info, parse_mode="HTML")
            else:
                await message.answer(f"❌ Користувача <code>@{username}</code> не знайдено.")
    except Exception as e:
        logging.error(f"Помилка в whois: {e}")
        await message.answer("❌ Сталася помилка при зверненні до БД.")

@router.message(Command("role"))
async def change_role(message: types.Message, command: CommandObject):
    if message.from_user.id != MY_TELEGRAM_ID:
        return 

    args = command.args.split() if command.args else []
    if len(args) < 2:
        await message.answer("❌ Використання: /role <ID> <роль>")
        return

    target_id = args[0]
    new_role = args[1]

    if not target_id.isdigit():
        await message.answer("❌ ID має бути числом!")
        return

    try:
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.telegram_id == int(target_id)))
            
            if user:
                user.role = new_role
                await session.commit()
                await message.answer(f"✅ Роль змінено на <b>{new_role}</b>.")
            else:
                await message.answer("❌ Користувача не знайдено.")
    except Exception as e:
        logging.error(f"Помилка в role: {e}")
        await message.answer("❌ Помилка під час запису в БД.")