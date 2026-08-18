from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from app.db.session import async_session
from app.models.order import Order

router = Router()


def _build_summary_text(data: dict) -> str:
    """Внутренняя совместимость для тестов и будущих расширений."""
    return (
        "📦 Нове замовлення\n\n"
        f"📌 Назва проєкту: {data.get('project_name', '—')}\n"
        f"📝 Додаткові побажання: {data.get('wishes', '—')}\n"
        f"📅 Дедлайн: {data.get('deadline', '—')}\n"
        f"💰 Бюджет: {data.get('budget', '—')}"
    )

@router.message(F.text.startswith("📋 Активні замовлення"))
async def show_active_it_orders(message: types.Message):
    """
    Виводить список замовлень, які зараз знаходяться в роботі або на доопрацюванні.
    """
    async with async_session() as session:
        result = await session.execute(
            select(Order).filter(Order.status.in_(["in_work", "revision"])).order_by(Order.id.desc())
        )
        orders = result.scalars().all()

    if not orders:
        return await message.answer("ℹ️ Наразі немає замовлень у роботі чи на доопрацюванні.")

    builder = InlineKeyboardBuilder()
    for ord_obj in orders:
        status_emoji = "👨‍💻" if ord_obj.status == "in_work" else "🔄"
        status_name = "В роботі" if ord_obj.status == "in_work" else "На доопрацюванні"
        
        desc_preview = ord_obj.description[:25] if ord_obj.description else "Без опису"
        
        builder.button(
            text=f"{status_emoji} #{ord_obj.id} | {desc_preview}... ({status_name})",
            callback_data=f"it_order_view:{ord_obj.id}"
        )
    
    builder.adjust(1)
    await message.answer(
        "🛠 <b>Список активних ІТ-замовлень:</b>\n"
        "Виберіть замовлення зі списку нижче для перегляду деталей:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("it_order_view:"))
async def view_it_order_detail(callback: types.CallbackQuery):
    order_id = int(callback.data.split(":")[1])

    async with async_session() as session:
        result = await session.execute(select(Order).filter(Order.id == order_id))
        order = result.scalar_one_or_none()

    if not order:
        return await callback.answer("❌ Замовлення не знайдено!", show_alert=True)

    status_name = "В роботі 👨‍💻" if order.status == "in_work" else "На доопрацюванні 🔄"

    text = (
        f"📦 <b>Замовлення #{order.id}</b>\n\n"
        f"📌 Назва / Опис: {order.description}\n"
        f"📊 Поточний статус: <b>{status_name}</b>\n"
        f"👤 ID менеджера / клієнта: <code>{order.user_id}</code>"
    )

    kb = InlineKeyboardBuilder()
    if order.status == "in_work":
        kb.button(text="🔄 Перевести на доопрацювання", callback_data=f"set_status:{order.id}:revision")
        kb.button(text="🏁 Завершити замовлення", callback_data=f"set_status:{order.id}:completed")
    elif order.status == "revision":
        kb.button(text="🛠 Повернути в роботу", callback_data=f"set_status:{order.id}:in_work")
        kb.button(text="🏁 Завершити замовлення", callback_data=f"set_status:{order.id}:completed")
    
    kb.button(text="🔙 Назад до списку", callback_data="back_to_active_orders")
    kb.adjust(1)

    await callback.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "back_to_active_orders")
async def back_to_active_orders_list(callback: types.CallbackQuery):
    async with async_session() as session:
        result = await session.execute(
            select(Order).filter(Order.status.in_(["in_work", "revision"])).order_by(Order.id.desc())
        )
        orders = result.scalars().all()

    if not orders:
        return await callback.message.edit_text("ℹ️ Наразі немає замовлень у роботі чи на доопрацюванні.")

    builder = InlineKeyboardBuilder()
    for ord_obj in orders:
        status_emoji = "👨‍💻" if ord_obj.status == "in_work" else "🔄"
        status_name = "В роботі" if ord_obj.status == "in_work" else "На доопрацюванні"
        
        desc_preview = ord_obj.description[:25] if ord_obj.description else "Без опису"
        
        builder.button(
            text=f"{status_emoji} #{ord_obj.id} | {desc_preview}... ({status_name})",
            callback_data=f"it_order_view:{ord_obj.id}"
        )
    
    builder.adjust(1)
    await callback.message.edit_text(
        "🛠 <b>Список активних ІТ-замовлень:</b>\n"
        "Виберіть замовлення зі списку нижче для перегляду деталей:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()