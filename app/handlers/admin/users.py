from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from app.db.session import async_session
from app.models.log import SystemLog
from app.models.user import User
from app.models.moderation import UserModeration

router = Router()


class AdminModeration(StatesGroup):
    waiting_warning_reason = State()
    waiting_ban_reason = State()
    waiting_unban_reason = State()


def _get_user_value(user_data, key, default="—"):
    if user_data is None:
        return default
    if hasattr(user_data, key):
        value = getattr(user_data, key, None)
        return value if value is not None else default
    if isinstance(user_data, dict):
        return user_data.get(key, default)
    return default


def build_user_moderation_text(user_data, moderation, history):
    history_lines = []
    if history:
        for item in history:
            created_at = item.get("created_at", "—") if isinstance(item, dict) else getattr(item, "created_at", "—")
            action = item.get("action", "action") if isinstance(item, dict) else getattr(item, "action", "action")
            details = item.get("details", "—") if isinstance(item, dict) else getattr(item, "details", "—")
            history_lines.append(f"• {created_at} | {action}: {details}")
    else:
        history_lines.append("• Немає історії модерації")

    warnings = moderation.warnings if moderation else 0
    is_banned = moderation.is_banned if moderation else False
    ban_reason = moderation.ban_reason if moderation else None

    full_name = _get_user_value(user_data, "full_name")
    telegram_id = _get_user_value(user_data, "telegram_id")
    username = _get_user_value(user_data, "username")
    role = _get_user_value(user_data, "role")

    return (
        f"👤 <b>{full_name}</b>\n"
        f"🆔 Telegram: {telegram_id}\n"
        f"@{username}\n"
        f"🎭 Роль: {role}\n"
        f"⚠️ Попереджень: {warnings}\n"
        f"🚦 Статус: {'🔴 Заблокований' if is_banned else '🟢 Активний'}\n"
        f"📝 Причина бану: {ban_reason or '—'}\n\n"
        f"<b>Історія модерації:</b>\n"
        + "\n".join(history_lines)
    )


async def get_moderation_history(session, user_id, limit=5):
    try:
        result = await session.execute(
            select(SystemLog)
            .where(SystemLog.user_id == user_id)
            .where(SystemLog.action.startswith("moderation_"))
            .order_by(SystemLog.created_at.desc())
            .limit(limit)
        )
        rows = result.scalars().all()
        return [
            {
                "action": row.action.replace("moderation_", ""),
                "details": row.details,
                "created_at": row.created_at.strftime("%d.%m %H:%M") if row.created_at else "—",
            }
            for row in rows
        ]
    except Exception:
        return []


def _extract_user_id(callback_data: str, prefix: str) -> int:
    data = callback_data[len(prefix):]
    if data.startswith("_"):
        data = data[1:]
    if data.startswith("user_"):
        data = data[5:]
    return int(data)


async def render_users_list(message_or_callback):
    async with async_session() as session:
        users = (await session.execute(select(User).order_by(User.full_name.asc()))).scalars().all()

        builder = InlineKeyboardBuilder()
        for user in users:
            try:
                mod = await session.get(UserModeration, user.telegram_id)
                status = "🔴" if mod and mod.is_banned else "🟢"
                warnings = mod.warnings if mod else 0
            except Exception:
                status = "🟢"
                warnings = 0

            label = f"{status} {user.full_name} | {user.role} | ⚠️ {warnings}"
            builder.button(text=label, callback_data=f"user_info_{user.telegram_id}")
        
        builder.button(text="🔙 Назад", callback_data="admin_panel")
        builder.adjust(1)

    text = "👥 <b>Список користувачів:</b>\nВиберіть профіль для перегляду або модерації."
    
    if isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
        await message_or_callback.answer()
    else:
        await message_or_callback.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")


@router.message(F.text == "🛠 Модерація")
async def open_moderation_menu(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="👥 Список користувачів", callback_data="admin_users_list")
    builder.adjust(1)
    await message.answer(
        "🛠 <b>Модерація</b>\nОберіть користувача для перегляду або дій.",
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "admin_users_list")
async def show_users_list_cb(callback: CallbackQuery):
    await render_users_list(callback)


@router.message(Command("db_list"))
async def show_users_list_cmd(message: Message):
    await render_users_list(message)


@router.callback_query(F.data.startswith("user_info_"))
async def show_user(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[2])
    
    async with async_session() as session:
        user = await session.get(User, user_id)
        if not user:
            await callback.answer("Користувача не знайдено в базі.", show_alert=True)
            return
        
        # Зберігаємо дані в звичайний словник, щоб уникнути проблеми з закриттям сесії
        user_data = {
            "telegram_id": user.telegram_id,
            "full_name": user.full_name,
            "username": user.username,
            "role": user.role,
        }
        
        mod = await session.get(UserModeration, user_id)
        history = await get_moderation_history(session, user_id)

    warnings_count = mod.warnings if mod else 0

    await callback.message.edit_text(
        build_user_moderation_text(user_data, mod, history),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"⚠️ Попередження ({warnings_count})", callback_data=f"warn_user_{user_id}")],
            [InlineKeyboardButton(text="🚫 Забанити", callback_data=f"ban_user_{user_id}")],
            [InlineKeyboardButton(text="🔓 Розбанити", callback_data=f"unban_user_{user_id}")],
            [InlineKeyboardButton(text="⬅️ Назад до списку", callback_data="admin_users_list")],
        ]),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("warn_"))
async def warn_user(callback: CallbackQuery, state: FSMContext):
    target_id = _extract_user_id(callback.data, "warn")
    await state.update_data(target_id=target_id)
    await state.set_state(AdminModeration.waiting_warning_reason)
    await callback.message.answer("⚠️ Введіть причину попередження:")
    await callback.answer()


@router.message(AdminModeration.waiting_warning_reason)
async def process_warn(message: Message, state: FSMContext):
    data = await state.get_data()
    target_id = int(data["target_id"])
    reason = message.text or "Без причини"
    
    async with async_session() as session:
        mod = await session.get(UserModeration, target_id)
        if not mod:
            mod = UserModeration(telegram_id=target_id, warnings=0, is_banned=False)
            session.add(mod)
        
        mod.warnings += 1
        
        log = SystemLog(user_id=target_id, action="moderation_warn", details=f"Попередження: {reason}")
        session.add(log)
        await session.commit()
        warnings_count = mod.warnings

    await message.answer(f"✅ Попередження додано. Кількість попереджень: {warnings_count}")
    await state.clear()


@router.callback_query(F.data.startswith("ban_"))
async def start_ban(callback: CallbackQuery, state: FSMContext):
    target_id = _extract_user_id(callback.data, "ban")
    async with async_session() as session:
        mod = await session.get(UserModeration, target_id)
        if mod and mod.is_banned:
            await callback.answer("Користувач уже заблокований.", show_alert=True)
            return

    await state.update_data(target_id=target_id)
    await state.set_state(AdminModeration.waiting_ban_reason)
    await callback.message.answer("🚫 Введіть причину бану:")
    await callback.answer()


@router.message(AdminModeration.waiting_ban_reason)
async def process_ban(message: Message, state: FSMContext):
    data = await state.get_data()
    target_id = int(data["target_id"])
    reason = message.text or "Без причини"
    
    async with async_session() as session:
        mod = await session.get(UserModeration, target_id)
        if not mod:
            mod = UserModeration(telegram_id=target_id, warnings=0, is_banned=False)
            session.add(mod)
        
        mod.is_banned = True
        mod.ban_reason = reason
        
        log = SystemLog(user_id=target_id, action="moderation_ban", details=f"Забанено: {reason}")
        session.add(log)
        await session.commit()

    await message.answer("🚫 Користувача забанено.")
    await state.clear()


@router.callback_query(F.data.startswith("unban_"))
async def start_unban(callback: CallbackQuery, state: FSMContext):
    target_id = _extract_user_id(callback.data, "unban")
    async with async_session() as session:
        mod = await session.get(UserModeration, target_id)
        if not mod or not mod.is_banned:
            await callback.answer("Користувач уже не заблокований.", show_alert=True)
            return

    await state.update_data(target_id=target_id)
    await state.set_state(AdminModeration.waiting_unban_reason)
    await callback.message.answer("🔓 Введіть причину розбану:")
    await callback.answer()


@router.message(AdminModeration.waiting_unban_reason)
async def process_unban(message: Message, state: FSMContext):
    data = await state.get_data()
    target_id = int(data["target_id"])
    reason = message.text or "Без причини"
    
    async with async_session() as session:
        mod = await session.get(UserModeration, target_id)
        if mod:
            mod.is_banned = False
            mod.ban_reason = None
            
            log = SystemLog(user_id=target_id, action="moderation_unban", details=f"Розбанено: {reason}")
            session.add(log)
            await session.commit()

    await message.answer("✅ Користувача розбанено.")
    await state.clear()