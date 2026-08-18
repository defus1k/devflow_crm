from aiogram import F, Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import and_, select

from app.db.session import async_session
from app.models.order import Order
from app.models.user import User

router = Router()


async def _check_developer(callback: types.CallbackQuery) -> bool:
    async with async_session() as session:
        user = await session.get(User, callback.from_user.id)
    return bool(user and user.role == "developer")


@router.callback_query(F.data == "dev_my_orders")
async def list_developer_orders(callback: types.CallbackQuery):
    if not await _check_developer(callback):
        await callback.answer("❌ У вас недостатньо прав для цього розділу.", show_alert=True)
        return

    async with async_session() as session:
        query = select(Order).where(and_(Order.developer_id == callback.from_user.id, Order.status.in_(["in_progress", "under_review"])))
        result = await session.execute(query)
        my_orders = result.scalars().all()

    if not my_orders:
        await callback.message.answer("У вас поки немає активних замовлень.")
        await callback.answer()
        return

    builder = InlineKeyboardBuilder()
    for order in my_orders:
        builder.button(text=f"📂 #{order.id} - {order.title}", callback_data=f"dev_project_entry_{order.id}")
    builder.adjust(1)

    await callback.message.answer("💼 Ваші активні проєкти:", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("dev_order_details_"))
async def show_order_actions(callback: types.CallbackQuery):
    if not await _check_developer(callback):
        await callback.answer("❌ У вас недостатньо прав для цього розділу.", show_alert=True)
        return
    order_id = int(callback.data.split("_")[-1])
    builder = InlineKeyboardBuilder()
    builder.button(text="📤 Здати роботу", callback_data=f"dev_submit_{order_id}")
    builder.button(text="💬 Написати менеджеру", callback_data=f"dev_contact_manager_{order_id}")
    builder.button(text="🔙 Назад", callback_data="dev_my_orders")
    builder.adjust(1)
    await callback.message.answer(f"🛠 Деталі проєкту #{order_id}\n\nОберіть дію:", reply_markup=builder.as_markup())
    await callback.answer()