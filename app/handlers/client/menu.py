from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.handlers.client.create_order import OrderForm
from app.keyboards.client.order_keyboards import get_project_type_kb
from app.keyboards.client.menu import get_main_menu_kb


router = Router()


# ==========================
# 🚀 Створити замовлення
# ==========================

@router.message(F.text == "🚀 Створити замовлення")
async def start_order(
        message: Message,
        state: FSMContext
):

    await message.answer(
        "🚀 Оберіть тип розробки:",
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        "Оберіть платформу:",
        reply_markup=get_project_type_kb()
    )

    await state.set_state(
        OrderForm.project_type
    )


# ==========================
# 🤖 Telegram Bot
# ==========================

@router.message(
    OrderForm.project_type,
    F.text == "🤖 Telegram Bot"
)
async def select_telegram(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        project_type="Telegram Bot"
    )

    await message.answer(
        "🔥 Введіть назву проекту:",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(
        OrderForm.title
    )


# ==========================
# 🎮 Discord Bot
# ==========================

@router.message(
    OrderForm.project_type,
    F.text == "🎮 Discord Bot"
)
async def select_discord(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        project_type="Discord Bot"
    )

    await message.answer(
        "🔥 Введіть назву проекту:",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(
        OrderForm.title
    )


# ==========================
# ⬅️ Назад у меню
# ==========================

@router.message(
    OrderForm.project_type,
    F.text == "⬅️ Назад у меню"
)
async def back_to_menu(
        message: Message,
        state: FSMContext
):

    await state.clear()

    await message.answer(
        "🏠 Головне меню:",
        reply_markup=get_main_menu_kb()
    )