from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.review import Review
from sqlalchemy import select, update

router = Router()

@router.callback_query(F.data == "admin_reviews")
async def show_all_reviews(callback: types.CallbackQuery):
    async with async_session() as session:
        # Отримуємо останні відгуки для модерації
        result = await session.execute(select(Review).order_by(Review.created_at.desc()).limit(15))
        reviews = result.scalars().all()

    if not reviews:
        await callback.message.edit_text("💬 Відгуків ще немає.")
        return

    builder = InlineKeyboardBuilder()
    for review in reviews:
        builder.button(
            text=f"⭐ {review.rating} | #{review.order_id}", 
            callback_data=f"admin_review_manage_{review.id}"
        )
    builder.adjust(1)
    
    await callback.message.edit_text("🛡 **Модерація відгуків:**", reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(F.data.startswith("admin_review_manage_"))
async def manage_review(callback: types.CallbackQuery):
    review_id = int(callback.data.split("_")[3])
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑 Видалити (спам)", callback_data=f"admin_review_delete_{review_id}")
    builder.button(text="🔙 Назад", callback_data="admin_reviews")
    
    await callback.message.edit_text(
        f"📝 **Управління відгуком #{review_id}**\n\n"
        "Тут адміністратор може видалити відгук, якщо він порушує правила платформи.",
        reply_markup=builder.as_markup()
    )
    await callback.answer()