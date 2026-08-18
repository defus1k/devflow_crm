from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

REVIEWS_LINK = "https://t.me/reviews_botqwe"

@router.message(Command("reviews"))
@router.message(F.text == "⭐ Відгуки")
async def reviews(message: types.Message):

    builder = InlineKeyboardBuilder()

    builder.button(
        text="⭐ Перейти до відгуків",
        url=REVIEWS_LINK
    )

    await message.answer(
        "⭐ Тут ви можете переглянути всі відгуки наших клієнтів.",
        reply_markup=builder.as_markup()
    )