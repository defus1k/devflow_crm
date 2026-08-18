from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.review import Review # Припустима модель відгуків
from sqlalchemy import select

router = Router()

@router.callback_query(F.data == "owner_reviews")
async def show_reviews(callback: types.CallbackQuery):
    async with async_session() as session:
        # Отримуємо останні відгуки
        result = await session.execute(select(Review).order_by(Review.created_at.desc()).limit(10))
        reviews = result.scalars().all()

    if not reviews:
        await callback.message.edit_text("💬 Відгуків поки що немає.")
        return

    builder = InlineKeyboardBuilder()
    for review in reviews:
        # Відображаємо рейтинг зірочками
        stars = "⭐" * review.rating
        builder.button(text=f"{stars} | Замовлення #{review.order_id}", callback_data=f"review_view_{review.id}")
    builder.adjust(1)
    
    await callback.message.edit_text("⭐ **Останні відгуки клієнтів:**", reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(F.data.startswith("review_view_"))
async def view_single_review(callback: types.CallbackQuery):
    review_id = int(callback.data.split("_")[2])
    
    async with async_session() as session:
        review = await session.get(Review, review_id)
        
    if review:
        await callback.message.edit_text(
            f"📝 **Відгук до замовлення #{review.order_id}**\n\n"
            f"Рейтинг: {'⭐' * review.rating}\n"
            f"Коментар: {review.text}\n\n"
            "Ви можете використати цей відгук для мотивації команди.",
            reply_markup=InlineKeyboardBuilder([
                [types.InlineKeyboardButton(text="🔙 Назад", callback_data="owner_reviews")]
            ]).as_markup()
        )
    await callback.answer()