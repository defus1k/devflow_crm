from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

from sqlalchemy import select

from app.db.session import async_session
from app.models.user import User

from app.keyboards.common.main_menu import get_main_menu_kb

router = Router()


async def register_user(message: Message):
    async with async_session() as session:

        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )

        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name,
                role="client"
            )

            session.add(user)
            await session.commit()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await register_user(message)

    # Отримуємо роль з БД для клавіатури
    async with async_session() as session:
        user_db = await session.scalar(select(User).where(User.telegram_id == message.from_user.id))
        role = user_db.role if user_db else "client"
        if user_db is None:
            user_db = User(telegram_id=message.from_user.id, username=message.from_user.username, full_name=message.from_user.full_name, role="client")
            session.add(user_db)
            await session.commit()
            role = user_db.role

    welcome_text = (
    f"👋 Вітаємо, <b>{message.from_user.full_name}</b>!\n\n"
    "🚀 <b>Nexora BotForge</b>\n\n"
    "Наша компанія займається розробкою:\n"
    "• Telegram-ботів\n"
    "• Discord-ботів\n\n"

    "⏰ <b>Графік роботи нашої команди:</b>\n"
    "Ми на зв'язку та готові допомагати вам у наступні години:\n\n"
    "Пн – Пт: 10:00 – 22:00\n"
    "Сб – Нд: 10:00 – 20:00\n\n"

    "👇 <b>Для продовження роботи оберіть потрібний вам пункт меню:</b>"
)
    await message.answer(
        welcome_text,
        parse_mode="HTML",
        # ПЕРЕДАЄМО РОЛЬ СЮДИ:
        reply_markup=get_main_menu_kb(role=role) 
    )


@router.message(CommandStart(deep_link=True))
async def cmd_start_referral(
    message: Message,
    command: CommandObject,
    state: FSMContext,
):
    await state.clear()

    await register_user(message)

    ref_id = command.args

    text = (
        f"👋 Ласкаво просимо!\n\n"
        f"Вас запросив користувач з ID: <code>{ref_id}</code>"
        if ref_id
        else "👋 Ласкаво просимо до <b>Nexora BotForge</b>!"
    )

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=get_main_menu_kb()
    )