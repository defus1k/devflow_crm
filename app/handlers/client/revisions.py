from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.db.session import async_session
from app.models.order import Order
from sqlalchemy import select

router = Router()

class RevisionForm(StatesGroup):
    description = State()
    order_id = State()

@router.callback_query(F.data.startswith("revise_"))
async def start_revision(callback: types.CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split("_")[1])
    await state.update_data(order_id=order_id)
    
    await callback.message.answer("Опишіть, які саме правки необхідно внести:")
    await state.set_state(RevisionForm.description)
    await callback.answer()

@router.message(RevisionForm.description)
async def process_revision(message: types.Message, state: FSMContext):
    data = await state.get_data()
    order_id = data['order_id']
    
    async with async_session() as session:
        order = await session.get(Order, order_id)
        if order:
            order.status = "in_revision"
            # Тут можна додати логіку збереження тексту правки в окрему таблицю Revision
            await session.commit()
            
    await message.answer("✅ Ваші правки надіслано розробнику. Ми скоро оновимо результат.")
    await state.clear()