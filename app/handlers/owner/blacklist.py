from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.user import User
from sqlalchemy import select, update

router = Router()

@router.callback_query(F.data == "owner_blacklist")
async def show_blacklist(callback: types.CallbackQuery):
    async with async_session() as session:
        # Шукаємо користувачів з прапорцем is_banned
        result = await session.execute(select(User).where(User.is_banned == True))
        banned_users = result.scalars().all()

    if not banned_users:
        await callback.message.edit_text("✅ Чорний список порожній.")
        return

    builder = InlineKeyboardBuilder()
    for user in banned_users:
        builder.button(text=f"🚫 {user.full_name} ({user.role})", callback_data=f"unban_{user.telegram_id}")
    builder.adjust(1)
    
    await callback.message.edit_text("🚫 **Чорний список:**\nНатисніть на користувача, щоб розблокувати:", reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(F.data.startswith("unban_"))
async def unban_user(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    
    async with async_session() as session:
        await session.execute(
            update(User).where(User.telegram_id == user_id).values(is_banned=False)
        )
        await session.commit()
    
    await callback.message.answer(f"✅ Користувача {user_id} розблоковано.")
    await callback.answer()