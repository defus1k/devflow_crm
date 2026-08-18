from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.order import Order
from sqlalchemy import select, update

router = Router()

# 1. Головна кнопка "📋 Замовлення" (Reply)
@router.message(F.text == "📋 Замовлення")
async def show_orders_menu(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="📦 Активні замовлення", callback_data="admin_orders_list")
    builder.button(text="✅ Виконані", callback_data="admin_orders_completed")
    builder.adjust(1)
    
    await message.answer(
        "📋 <b>Управління замовленнями:</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

# Повернення до головного меню замовлень через callback
@router.callback_query(F.data == "orders_menu_main")
async def orders_menu_main_cb(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="📦 Активні замовлення", callback_data="admin_orders_list")
    builder.button(text="✅ Виконані", callback_data="admin_orders_completed")
    builder.adjust(1)
    
    await callback.message.edit_text(
        "📋 <b>Управління замовленнями:</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()

# 2. Список активних замовлень (Inline)
@router.callback_query(F.data == "admin_orders_list")
async def list_active_orders(callback: types.CallbackQuery):
    async with async_session() as session:
        result = await session.execute(select(Order).where(Order.status != "completed").limit(10))
        orders = result.scalars().all()
    
    if not orders:
        builder = InlineKeyboardBuilder()
        builder.button(text="🔙 Назад", callback_data="orders_menu_main")
        builder.adjust(1)
        await callback.message.edit_text("✅ Активних замовлень немає.", reply_markup=builder.as_markup(), parse_mode="HTML")
        return await callback.answer()
    
    builder = InlineKeyboardBuilder()
    for o in orders:
        builder.button(text=f"⚙️ Замовлення #{o.id}", callback_data=f"admin_order_view_{o.id}")
    
    builder.button(text="🔙 Назад", callback_data="orders_menu_main")
    builder.adjust(1)
    
    await callback.message.edit_text("📦 <b>Активні замовлення:</b>", reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

# 2.1. Список виконаних замовлень (Inline) — ДОДАНО
@router.callback_query(F.data == "admin_orders_completed")
async def list_completed_orders(callback: types.CallbackQuery):
    async with async_session() as session:
        result = await session.execute(select(Order).where(Order.status == "completed").limit(10))
        orders = result.scalars().all()
    
    if not orders:
        builder = InlineKeyboardBuilder()
        builder.button(text="🔙 Назад", callback_data="orders_menu_main")
        builder.adjust(1)
        await callback.message.edit_text("📁 Виконаних замовлень поки немає.", reply_markup=builder.as_markup(), parse_mode="HTML")
        return await callback.answer()
    
    builder = InlineKeyboardBuilder()
    for o in orders:
        builder.button(text=f"✅ Замовлення #{o.id}", callback_data=f"admin_order_view_{o.id}")
    
    builder.button(text="🔙 Назад", callback_data="orders_menu_main")
    builder.adjust(1)
    
    await callback.message.edit_text("✅ <b>Виконані замовлення:</b>", reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

# 3. Перегляд деталей конкретного замовлення
@router.callback_query(F.data.startswith("admin_order_view_"))
async def view_order(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_")[3])
    
    async with async_session() as session:
        order = await session.scalar(select(Order).where(Order.id == order_id))
    
    if not order:
        return await callback.answer("❌ Замовлення не знайдено.", show_alert=True)

    builder = InlineKeyboardBuilder()
    # Якщо замовлення ще не виконане, показуємо кнопку завершення
    if order.status != "completed":
        builder.button(text="✅ Відзначити як виконане", callback_data=f"admin_order_done_{order_id}")
    
    builder.button(text="🔙 Назад до списку", callback_data="admin_orders_list" if order.status != "completed" else "admin_orders_completed")
    builder.adjust(1)
    
    text = (
        f"📋 <b>Замовлення #{order.id}</b>\n\n"
        f"Статус: {order.status}\n"
        f"Бюджет: {order.budget} грн\n"
        f"Дата: {order.created_at.strftime('%d.%m.%Y')}"
    )
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

# 4. Дія: Відзначити як виконане
@router.callback_query(F.data.startswith("admin_order_done_"))
async def complete_order(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_")[3])
    
    async with async_session() as session:
        await session.execute(update(Order).where(Order.id == order_id).values(status="completed"))
        await session.commit()
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 До списку активних", callback_data="admin_orders_list")
    builder.adjust(1)

    await callback.answer("✅ Замовлення успішно завершено!")
    await callback.message.edit_text("✅ Замовлення виконано та перенесено до архіву.", reply_markup=builder.as_markup())