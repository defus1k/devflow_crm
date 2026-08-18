from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.user import User
from sqlalchemy import select, update

router = Router()

@router.callback_query(F.data.startswith("admin_warn_"))
async def warn_user(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[2])
    
    async with async_session() as session:
        # Збільшуємо лічильник попереджень (припустимо, є поле warnings_count)
        user = await session.get(User, user_id)
        if user:
            user.warnings_count += 1
            await session.commit()
            
            # Повідомляємо користувача
            await callback.bot.send_message(
                user.telegram_id, 
                f"⚠️ **Попередження від адміністрації!**\n\n"
                f"Причина: Порушення правил системи.\n"
                f"Ваш рахунок попереджень: {user.warnings_count}. "
                "Наступні порушення призведуть до блокування."
            )
            
    await callback.message.answer(f"✅ Попередження успішно надіслано користувачу {user_id}.")
    await callback.answer()