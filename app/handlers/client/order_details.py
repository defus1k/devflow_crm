from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.order import Order
from sqlalchemy import select

router = Router()

@router.callback_query(F.data.startswith("details_"))
async def show_full_details(callback: types.CallbackQuery):
    """
    Виводить розширену інформацію про замовлення з додатковими діями.
    """
    order_id = int(callback.data.split("_")[1])
    
    async with async_session() as session:
        result = await session.execute(select(Order).filter(Order.id == order_id))
        order = result.scalar_one_or_none()
    
    if not order:
        await callback.answer("Замовлення не знайдено.")
        return

    # Створюємо меню дій для замовлення
    builder = InlineKeyboardBuilder()
    builder.button(text="💳 Оплатити", callback_data=f"pay_{order.id}")
    builder.button(text="🔄 Запросити правки", callback_data=f"revise_{order.id}")
    builder.button(text="⬅️ Назад до списку", callback_data="back_to_orders")
    builder.adjust(2)

    text = (
        f"📋 **Замовлення: {order.title}**\n\n"
        f"📝 Опис: {order.description}\n"
        f"💰 Бюджет: {order.budget} USD\n"
        f"⚙️ Статус: {order.status}\n"
        f"📅 Створено: {order.created_at.strftime('%d.%m.%Y')}"
    )
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()