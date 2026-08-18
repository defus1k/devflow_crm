from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.order import Order
from sqlalchemy import select

router = Router()

@router.message(Command("my_orders"))
async def list_my_orders(message: types.Message):
    """
    Виводить список замовлень користувача з БД.
    """
    async with async_session() as session:
        # Шукаємо всі замовлення цього користувача
        query = select(Order).filter(Order.user_id == message.from_user.id)
        result = await session.execute(query)
        orders = result.scalars().all()

    if not orders:
        await message.answer("У вас поки що немає активних замовлень.")
        return

    builder = InlineKeyboardBuilder()
    for order in orders:
        # Додаємо кнопку для кожного замовлення
        builder.button(
            text=f"📦 {order.title} ({order.status})", 
            callback_data=f"order_view_{order.id}"
        )
    
    builder.adjust(1)
    await message.answer("Ваші замовлення:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("order_view_"))
async def show_order_details(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_")[2])
    
    async with async_session() as session:
        result = await session.execute(select(Order).filter(Order.id == order_id))
        order = result.scalar_one_or_none()
    
    if order:
        await callback.message.answer(
            f"ℹ️ **Деталі замовлення #{order.id}**\n\n"
            f"Назва: {order.title}\n"
            f"Опис: {order.description}\n"
            f"Бюджет: {order.budget} USD\n"
            f"Статус: {order.status}"
        )
    await callback.answer()