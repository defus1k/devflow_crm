from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.db.session import async_session
from app.models.order import Order
from sqlalchemy import select

router = Router()

class BriefingForm(StatesGroup):
    edit_description = State()

@router.callback_query(F.data.startswith("brief_"))
async def start_briefing(callback: types.CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split("_")[1])
    await state.update_data(order_id=order_id)
    
    await callback.message.answer("Введіть відкориговане технічне завдання для розробника:")
    await state.set_state(BriefingForm.edit_description)
    await callback.answer()

@router.message(BriefingForm.edit_description)
async def process_brief(message: types.Message, state: FSMContext):
    data = await state.get_data()
    order_id = data['order_id']
    
    async with async_session() as session:
        order = await session.get(Order, order_id)
        if order:
            order.description = message.text
            order.status = "briefing_approved" # Статус: готово до взяття в роботу
            await session.commit()
            
    await message.answer("✅ ТЗ успішно оновлено та надіслано в чергу для розробників.")
    await state.clear()