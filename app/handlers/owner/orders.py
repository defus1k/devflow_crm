from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.order import Order
from sqlalchemy import select

router = Router()

@router.callback_query(F.data == "owner_orders")
async def show_all_orders(callback: types.CallbackQuery):
    async with async_session() as session:
        # Вибираємо всі замовлення, сортуємо за новизною
        query = select(Order).order_by(Order.created_at.desc()).limit(20)
        result = await session.execute(query)
        orders = result.scalars().all()

    if not orders:
        await callback.message.answer("Замовлень ще немає.")
        return

    builder = InlineKeyboardBuilder()
    for order in orders:
        status_emoji = "✅" if order.status == "completed" else "⏳"
        builder.button(
            text=f"{status_emoji} #{order.id} | {order.title}", 
            callback_data=f"owner_view_{order.id}"
        )
    builder.adjust(1)
    
    await callback.message.answer("📋 **Всі замовлення в системі:**", reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(F.data.startswith("owner_view_"))
async def view_order_details(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_")[2])
    async with async_session() as session:
        order = await session.get(Order, order_id)
        
    if order:
        await callback.message.answer(
            f"👑 **Контроль замовлення #{order.id}**\n\n"
            f"Назва: {order.title}\n"
            f"Статус: {order.status}\n"
            f"Бюджет: {order.budget} USD\n"
            f"ID розробника: {order.developer_id or 'Не призначено'}\n\n"
            "Ви можете передати це замовлення іншому менеджеру або скасувати його."
        )
    await callback.answer()