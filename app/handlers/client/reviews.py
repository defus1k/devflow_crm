from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.review import Review
from sqlalchemy import select

router = Router()

class ReviewForm(StatesGroup):
    rating = State()
    text = State()

@router.message(F.text == "⭐ Відгуки")
async def start_review(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    for i in range(1, 6):
        builder.button(text="⭐" * i, callback_data=f"rating_{i}")
    builder.adjust(1)
    
    await message.answer("Оцініть нашу роботу від 1 до 5 зірок:", reply_markup=builder.as_markup())
    await state.set_state(ReviewForm.rating)

@router.callback_query(ReviewForm.rating, F.data.startswith("rating_"))
async def process_rating(callback: types.CallbackQuery, state: FSMContext):
    rating = int(callback.data.split("_")[1])
    await state.update_data(rating=rating)
    await callback.message.answer("Дякуємо! Напишіть кілька слів про співпрацю:")
    await state.set_state(ReviewForm.text)
    await callback.answer()

@router.message(ReviewForm.text)
async def process_review_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    async with async_session() as session:
        new_review = Review(
            user_id=message.from_user.id,
            rating=data['rating'],
            text=message.text
        )
        session.add(new_review)
        await session.commit()
    
    await message.answer("✅ Дякуємо за ваш відгук! Він дуже допомагає нам ставати кращими.")
    await state.clear()