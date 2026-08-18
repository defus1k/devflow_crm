from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.db.session import async_session
from app.models.ticket import Ticket

router = Router()

# Визначаємо стан для створення тікета
class SupportForm(StatesGroup):
    waiting_for_subject = State()
    waiting_for_description = State()

@router.message(Command("support"))
async def cmd_support(message: types.Message, state: FSMContext):
    await message.answer("Опишіть коротко тему вашого звернення:")
    await state.set_state(SupportForm.waiting_for_subject)

@router.message(SupportForm.waiting_for_subject)
async def process_subject(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("Тепер детально опишіть вашу проблему:")
    await state.set_state(SupportForm.waiting_for_description)

@router.message(SupportForm.waiting_for_description)
async def process_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    subject = data.get("subject")
    description = message.text
    
    # Зберігаємо в базу даних
    async with async_session() as session:
        new_ticket = Ticket(
            user_id=message.from_user.id,
            subject=subject,
            description=description,
            status="open"
        )
        session.add(new_ticket)
        await session.commit()
    
    await message.answer("✅ Ваше звернення прийнято! Менеджер скоро відповість.")
    await state.clear()