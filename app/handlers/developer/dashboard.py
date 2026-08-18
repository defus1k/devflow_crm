from aiogram import Router, F, types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select, func

from app.db.session import async_session
from app.models.order import Order
from app.models.user import User

router = Router()


# ==================================================
# 🚀 ВЗЯТИ ЗАМОВЛЕННЯ (Кнопка у форумному топіку)
# ==================================================

@router.callback_query(F.data.startswith("take_order:"))
async def take_order_callback(callback: types.CallbackQuery):
    parts = callback.data.split(":")
    if len(parts) < 3:
        await callback.answer("❌ Помилка: неповні дані замовлення!", show_alert=True)
        return
    _, order_id, client_id = parts[:3]
    
    async with async_session() as session:
        order = await session.get(Order, int(order_id))
        if order:
            order.developer_id = callback.from_user.id
            order.status = "in_work"
            await session.commit()
            
    try:
        await callback.message.edit_text(
            text=callback.message.text + f"\n\n✅ <b>Взяв в роботу розробник:</b> @{callback.from_user.username or callback.from_user.full_name}", 
            parse_mode="HTML"
        )
    except Exception:
        pass
    
    await callback.answer("✅ Ви успішно взяли замовлення в роботу!", show_alert=True)


# ==================================================
# 📥 НОВІ ЗАМОВЛЕННЯ
# ==================================================

@router.message(F.text == "📥 Нові замовлення")
async def new_orders(message: types.Message):
    async with async_session() as session:
        result = await session.scalars(
            select(Order)
            .where(
                Order.developer_id.is_(None),
                Order.status.in_(["pending", "new", "in_work"])
            )
        )
        orders = result.all()

    if not orders:
        await message.answer("📥 Нових доступних замовлень немає.")
        return

    for order in orders:
        kb = InlineKeyboardBuilder()
        kb.button(
            text=f"📌 Замовлення #{order.id}",
            callback_data=f"dev_order_{order.id}"
        )
        await message.answer(
            f"🆔 Доступне замовлення #{order.id}",
            reply_markup=kb.as_markup()
        )


# ==================================================
# 📌 ВІДКРИТИ ЗАМОВЛЕННЯ
# ==================================================

@router.callback_query(F.data.startswith("dev_order_"))
async def open_order(callback: types.CallbackQuery):
    try:
        order_id = int(callback.data.replace("dev_order_", ""))
    except ValueError:
        await callback.answer("❌ Помилка обробки замовлення.", show_alert=True)
        return

    await callback.message.answer(
        f"""
📌 <b>Замовлення #{order_id}</b>

Переглянути деталі можна у форумі розробників.
Знайдіть тему: <b>Замовлення №{order_id}</b>

Там знаходиться:
• опис проекту
• бюджет
• контакти
• технічне завдання
""",
        parse_mode="HTML"
    )
    await callback.answer()


# ==================================================
# 💼 МОЇ ПРОЄКТИ
# ==================================================

@router.message(F.text == "💼 Мої проєкти")
async def my_projects(message: types.Message):
    async with async_session() as session:
        result = await session.scalars(
            select(Order)
            .where(Order.developer_id == message.from_user.id)
            .where(
                Order.status.in_([
                    "pending",
                    "new",
                    "in_work",
                    "in_progress",
                    "review"
                ])
            )
        )
        orders = result.all()

    if not orders:
        await message.answer("💼 У вас немає активних проектів.")
        return

    kb = InlineKeyboardBuilder()
    for order in orders:
        kb.button(
            text=f"📌 #{order.id}",
            callback_data=f"my_project_{order.id}"
        )
    kb.adjust(1)

    await message.answer(
        "💼 Ваші активні проекти:",
        reply_markup=kb.as_markup()
    )


@router.callback_query(F.data.startswith("my_project_"))
async def my_project(callback: types.CallbackQuery):
    try:
        order_id = int(callback.data.replace("my_project_", ""))
    except ValueError:
        await callback.answer("❌ Помилка.", show_alert=True)
        return

    await callback.message.answer(
        f"""
📌 <b>Проект #{order_id}</b>

Відкрийте форум розробників.
Там знаходиться повна інформація по замовленню.
""",
        parse_mode="HTML"
    )
    await callback.answer()


# ==================================================
# 📤 ЗДАТИ РОБОТУ
# ==================================================

# ==================================================
# 📤 ЗДАТИ РОБОТУ
# ==================================================

@router.message(F.text == "📤 Здати роботу")
async def submit_menu(message: types.Message):
    async with async_session() as session:
        result = await session.scalars(
            select(Order)
            .where(Order.developer_id == message.from_user.id)
            .where(Order.status.notin_(["completed", "review"])) # Виключаємо здані та завершені
        )
        orders = result.all()

    if not orders:
        await message.answer("📤 У вас немає активних проєктів, які очікують на здачу.")
        return

    kb = InlineKeyboardBuilder()
    for order in orders:
        kb.button(
            text=f"📤 Здати #{order.id}",
            callback_data=f"submit_{order.id}"
        )
    kb.adjust(1)

    await message.answer(
        "Оберіть проєкт для здачі:",
        reply_markup=kb.as_markup()
    )


@router.callback_query(F.data.startswith("submit_"))
async def submit_work(callback: types.CallbackQuery, bot: Bot):
    try:
        order_id = int(callback.data.replace("submit_", ""))
    except ValueError:
        await callback.answer("❌ Помилка.", show_alert=True)
        return

    async with async_session() as session:
        order = await session.get(Order, order_id)
        
        if not order:
            await callback.answer("❌ Замовлення не знайдено.", show_alert=True)
            return

        if order.developer_id != callback.from_user.id:
            await callback.answer("❌ Це не ваш проєкт!", show_alert=True)
            return

        if order.status in ["review", "completed"]:
            await callback.answer("❌ Цей проєкт вже здано або завершено!", show_alert=True)
            return

        order.status = "review"
        await session.commit()

        manager_id = order.user_id
        forum_topic_id = getattr(order, "forum_topic_id", None)

    developer = callback.from_user
    dev_mention = f"@{developer.username}" if developer.username else developer.full_name

    if manager_id:
        try:
            await bot.send_message(
                chat_id=manager_id,
                text=f"📤 <b>Розробник {dev_mention} здав роботу по проєкту #{order_id}!</b>\nОчікує на перевірку.",
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Не вдалося сповістити менеджера: {e}")

    if forum_topic_id:
        try:
            await bot.send_message(
                chat_id=callback.message.chat.id,
                message_thread_id=forum_topic_id,
                text=f"📤 <b>Роботу по проєкту #{order_id} здано розробником {dev_mention}!</b> Очікує перевірки менеджера.",
                parse_mode="HTML"
            )
        except Exception:
            pass

    await callback.message.answer(
        f"""
✅ <b>Проєкт #{order_id} успішно здано.</b>

Менеджер отримав сповіщення.
Очікуйте перевірки.
""",
        parse_mode="HTML"
    )
    await callback.answer("✅ Проєкт успішно здано!", show_alert=True)


# ==================================================
# 💬 ЧАТ З МЕНЕДЖЕРОМ
# ==================================================

@router.message(F.text == "💬 Чат з менеджером")
async def manager_chat(message: types.Message):
    async with async_session() as session:
        result = await session.scalars(
            select(Order)
            .where(Order.developer_id == message.from_user.id)
        )
        orders = result.all()

    if not orders:
        await message.answer("💬 У вас немає проектів з менеджером.")
        return

    kb = InlineKeyboardBuilder()
    for order in orders:
        kb.button(
            text=f"💬 #{order.id}",
            callback_data=f"manager_{order.id}"
        )
    kb.adjust(1)

    await message.answer(
        "Оберіть проект:",
        reply_markup=kb.as_markup()
    )


@router.callback_query(F.data.startswith("manager_"))
async def manager_info(callback: types.CallbackQuery):
    try:
        order_id = int(callback.data.replace("manager_", ""))
    except ValueError:
        await callback.answer("❌ Помилка.", show_alert=True)
        return

    async with async_session() as session:
        order = await session.get(Order, order_id)
        manager = None

        if order and order.user_id:
            manager = await session.scalar(
                select(User)
                .where(User.telegram_id == order.user_id)
            )

    if manager:
        username_display = f"@{manager.username}" if manager.username else "відсутній"
        text = f"""
💬 <b>Менеджер проекту #{order_id}</b>

👤 Ім'я: {manager.full_name}
📱 Юзернейм: {username_display}
"""
    else:
        text = f"""
💬 <b>Проект #{order_id}</b>

⚠️ Менеджер ще не призначений або дані про нього відсутні в системі.
"""

    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()


# ==================================================
# 📊 СТАТИСТИКА
# ==================================================

@router.message(F.text == "📊 Моя статистика")
async def statistics(message: types.Message):
    async with async_session() as session:
        total = await session.scalar(
            select(func.count(Order.id))
            .where(Order.developer_id == message.from_user.id)
        ) or 0

        completed = await session.scalar(
            select(func.count(Order.id))
            .where(
                Order.developer_id == message.from_user.id,
                Order.status == "completed"
            )
        ) or 0

        money = await session.scalar(
            select(func.sum(Order.budget))
            .where(
                Order.developer_id == message.from_user.id,
                Order.status == "completed"
            )
        ) or 0

        active = await session.scalar(
            select(func.count(Order.id))
            .where(
                Order.developer_id == message.from_user.id,
                Order.status.in_([
                    "in_work",
                    "in_progress",
                    "review"
                ])
            )
        ) or 0

    await message.answer(
        f"""
📊 <b>Статистика розробника</b>

👤 Користувач:
{message.from_user.full_name}

━━━━━━━━━━━━━━

📦 Всього проектів:
<b>{total}</b>

⚙️ Активних:
<b>{active}</b>

✅ Завершено:
<b>{completed}</b>

💰 Зароблено:
<b>{money} грн</b>

📈 Середній чек:
<b>{round(money / completed, 2) if completed else 0} грн</b>

━━━━━━━━━━━━━━

🚀 Продовжуйте виконувати проекти!
""",
        parse_mode="HTML"
    )