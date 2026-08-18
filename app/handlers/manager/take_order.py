from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.db.session import async_session
from app.models.order import Order
from sqlalchemy import select

router = Router()

class AssignmentForm(StatesGroup):
    waiting_for_dev_id = State()

@router.callback_query(F.data.startswith("assign_dev_"))
async def start_assignment(callback: types.CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split("_")[2])
    await state.update_data(order_id=order_id)
    
    await callback.message.answer("Введіть Telegram ID розробника для призначення на цей проєкт:")
    await state.set_state(AssignmentForm.waiting_for_dev_id)
    await callback.answer()

@router.message(AssignmentForm.waiting_for_dev_id)
async def process_assignment(message: types.Message, state: FSMContext):
    dev_id = message.text.strip()
    data = await state.get_data()
    order_id = data['order_id']
    
    async with async_session() as session:
        order = await session.get(Order, order_id)
        if order:
            order.developer_id = dev_id
            order.status = "in_progress"
            await session.commit()
            
    await message.answer(f"✅ Розробник {dev_id} призначений на замовлення #{order_id}!")
    await state.clear()