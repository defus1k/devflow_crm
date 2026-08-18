from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from app.db.session import async_session
from app.models.order import Order

router = Router()


@router.callback_query(F.data == "manager_my_orders")
async def list_active_orders(callback: types.CallbackQuery):
    async with async_session() as session:
        query = select(Order).filter(Order.manager_id == callback.from_user.id)
        result = await session.execute(query)
        orders = result.scalars().all()

    if not orders:
        await callback.message.answer("У вас поки немає замовлень.")
        return

    builder = InlineKeyboardBuilder()
    for order in orders:
        builder.button(text=f"🛠 #{order.id} | {order.title}", callback_data=f"manager_order_view_{order.id}")
    builder.adjust(1)

    await callback.message.answer("📦 Ваші замовлення:", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("manager_order_view_"))
async def show_manager_order_details(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_")[-1])

    async with async_session() as session:
        order = await session.get(Order, order_id)

    if not order:
        await callback.answer("❌ Замовлення не знайдено.", show_alert=True)
        return

    text = (
        f"📋 Деталі замовлення #{order.id}\n\n"
        f"Назва: {order.title}\n"
        f"Категорія: {order.project_type}\n"
        f"Статус: {order.status}\n"
        f"Розробник: {order.developer_id or 'не призначено'}\n"
        f"Опис: {order.description}"
    )
    await callback.message.answer(text)
    await callback.answer()