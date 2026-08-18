from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.user import User
from sqlalchemy import select, update

router = Router()

@router.callback_query(F.data == "admin_blacklist")
async def show_blacklist(callback: types.CallbackQuery):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.is_banned == True))
        banned_users = result.scalars().all()

    if not banned_users:
        await callback.message.edit_text("✅ Чорний список порожній.")
        return

    builder = InlineKeyboardBuilder()
    for user in banned_users:
        builder.button(text=f"🚫 {user.full_name}", callback_data=f"admin_unban_{user.telegram_id}")
    builder.adjust(1)
    
    await callback.message.edit_text("🚫 **Чорний список:**\nНатисніть на користувача для розблокування:", reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(F.data.startswith("admin_unban_"))
async def unban_user(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[2])
    
    async with async_session() as session:
        await session.execute(
            update(User).where(User.telegram_id == user_id).values(is_banned=False)
        )
        await session.commit()
    
    await callback.message.answer(f"✅ Користувача {user_id} успішно розблоковано.")
    await callback.answer()