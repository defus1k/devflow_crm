from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.db.session import async_session
from app.models.config import Config # Припустима модель конфігурації
from sqlalchemy import select

router = Router()

class SettingsForm(StatesGroup):
    waiting_for_new_value = State()

@router.callback_query(F.data == "owner_settings")
async def show_settings(callback: types.CallbackQuery):
    async with async_session() as session:
        # Отримуємо поточні налаштування
        config = await session.execute(select(Config))
        conf = config.scalar()

    await callback.message.edit_text(
        f"⚙️ **Глобальні налаштування системи:**\n\n"
        f"🔹 Відсоток комісії: {conf.commission_rate}%\n"
        f"🔹 Мінімальний бюджет: {conf.min_budget} USD\n\n"
        "Натисніть на значення, щоб змінити його.",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="✏️ Змінити комісію", callback_data="set_commission")],
            [types.InlineKeyboardButton(text="🔙 Назад", callback_data="owner_dashboard")]
        ])
    )
    await callback.answer()

@router.callback_query(F.data == "set_commission")
async def ask_commission(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введіть нове значення комісії (у %):")
    await state.set_state(SettingsForm.waiting_for_new_value)
    await state.update_data(field="commission")
    await callback.answer()