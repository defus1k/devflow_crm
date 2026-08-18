from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from app.db.session import async_session
from app.models.user import User
from app.core.config import settings
from sqlalchemy import select

router = Router()

# Список ID користувачів, які мають право керувати ролями
ALLOWED_IDS = {settings.OWNER_ID}

# --- ФУНКЦІЯ ЗМІНИ РОЛІ ---
@router.message(Command("role"))
async def change_role(message: types.Message, command: CommandObject):
    if message.from_user.id not in ALLOWED_IDS:
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

    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == int(target_id)))
        
        if user:
            user.role = new_role
            await session.commit()
            await message.answer(f"✅ Роль користувача {user.full_name} змінено на <b>{new_role}</b>.")
        else:
            await message.answer("❌ Користувача з таким ID не знайдено в базі.")

# --- КОМАНДИ ПЕРЕМИКАННЯ ---
async def update_my_role(message: types.Message, new_role: str, role_display_name: str):
    if message.from_user.id not in ALLOWED_IDS:
        return

    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == message.from_user.id))
        if user:
            user.role = new_role
            await session.commit()
            await message.answer(f"⚡️ Вашу роль змінено на: <b>{role_display_name}</b>")

@router.message(Command("set_owner"))
async def set_owner(message: types.Message): await update_my_role(message, "owner", "👑 Власник")

@router.message(Command("set_admin"))
async def set_admin(message: types.Message): await update_my_role(message, "admin", "🛡 Адмін")

@router.message(Command("set_manager"))
async def set_manager(message: types.Message): await update_my_role(message, "manager", "💼 Менеджер")

@router.message(Command("set_dev"))
async def set_dev(message: types.Message): await update_my_role(message, "developer", "💻 Розробник")

@router.message(Command("set_client"))
async def set_client(message: types.Message): await update_my_role(message, "client", "👤 Клієнт")

# --- ЛИСТУВАННЯ ---
@router.message(Command("db_list"))
async def list_users(message: types.Message):
    if message.from_user.id not in ALLOWED_IDS: return
    async with async_session() as session:
        users = await session.execute(select(User))
        result = users.scalars().all()
        text = "📋 Список користувачів:\n"
        for u in result:
            text += f"• {u.full_name} | ID: <code>{u.telegram_id}</code> | Роль: {u.role}\n"
        await message.answer(text, parse_mode="HTML")