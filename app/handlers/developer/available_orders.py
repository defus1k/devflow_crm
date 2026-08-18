from __future__ import annotations

from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from app.db.session import async_session
from app.models.order import Order
from app.models.user import User


router = Router()


# ==========================
# Проверка разработчика
# ==========================

async def get_developer(user_id: int):

    async with async_session() as session:
        user = await session.get(User, user_id)

    if not user:
        return None

    if user.role != "developer":
        return None

    return user



# ==========================
# 📥 Нові замовлення
# ==========================

@router.message(F.text == "📥 Нові замовлення")
async def new_orders(message: types.Message):

    developer = await get_developer(message.from_user.id)

    if not developer:
        await message.answer(
            "❌ У вас немає доступу."
        )
        return


    async with async_session() as session:

        result = await session.execute(
            select(Order)
            .where(Order.status == "new")
        )

        orders = result.scalars().all()



    if not orders:
        await message.answer(
            "📦 Нових замовлень немає."
        )
        return



    kb = InlineKeyboardBuilder()


    for order in orders:

        kb.button(
            text=f"📌 #{order.id} {order.title}",
            callback_data=f"take_order_{order.id}"
        )


    kb.adjust(1)


    await message.answer(
        "📥 Доступні замовлення:",
        reply_markup=kb.as_markup()
    )



# ==========================
# Взяти замовлення
# ==========================

@router.callback_query(F.data.startswith("take_order_"))
async def take_order(callback: types.CallbackQuery):

    order_id = int(
        callback.data.split("_")[-1]
    )


    async with async_session() as session:

        order = await session.get(
            Order,
            order_id
        )


        if not order:
            await callback.answer(
                "Замовлення не знайдено",
                show_alert=True
            )
            return


        if order.developer_id:
            await callback.answer(
                "Замовлення вже взяв інший розробник",
                show_alert=True
            )
            return


        order.developer_id = callback.from_user.id
        order.status = "in_progress"


        await session.commit()



    await callback.message.answer(
        f"✅ Ви взяли замовлення #{order_id}"
    )

    await callback.answer()



# ==========================
# 💼 Мої проєкти
# ==========================

@router.message(F.text == "💼 Мої проєкти")
async def my_projects(message: types.Message):

    developer = await get_developer(message.from_user.id)

    if not developer:
        return



    async with async_session() as session:

        result = await session.execute(
            select(Order)
            .where(
                Order.developer_id == message.from_user.id
            )
        )

        orders = result.scalars().all()



    if not orders:

        await message.answer(
            "💼 У вас немає проєктів."
        )

        return



    text = "💼 Ваші проєкти:\n\n"


    for order in orders:

        text += (
            f"#{order.id}\n"
            f"📌 {order.title}\n"
            f"Статус: {order.status}\n\n"
        )


    await message.answer(text)



# ==========================
# 📤 Здати роботу
# ==========================

@router.message(F.text == "📤 Здати роботу")
async def submit_work(message: types.Message):

    developer = await get_developer(message.from_user.id)

    if not developer:
        return


    await message.answer(
        "📤 Надішліть файл або опис готової роботи.\n"
        "Менеджер перевірить результат."
    )



# ==========================
# 💬 Чат з менеджером
# ==========================

@router.message(F.text == "💬 Чат з менеджером")
async def manager_chat(message: types.Message):

    await message.answer(
        "💬 Чат з менеджером буде доступний після інтеграції."
    )



# ==========================
# 📊 Статистика
# ==========================

@router.message(F.text == "📊 Моя статистика")
async def stats(message: types.Message):


    async with async_session() as session:

        result = await session.execute(
            select(Order)
            .where(
                Order.developer_id == message.from_user.id
            )
        )

        orders = result.scalars().all()



    completed = len(
        [
            x for x in orders
            if x.status == "completed"
        ]
    )


    await message.answer(
        f"""
📊 Статистика:

Всього проєктів: {len(orders)}
Завершено: {completed}
"""
    )



# ==========================
# 👤 Особистий кабінет
# ==========================

@router.message(F.text == "👤 Особистий кабінет")
async def cabinet(message: types.Message):

    user = await get_developer(
        message.from_user.id
    )

    if not user:
        return


    await message.answer(
        f"""
👤 Особистий кабінет

Ім'я: {user.full_name}
Роль: Developer
"""
    )



# ==========================
# 📞 Підтримка
# ==========================

@router.message(F.text == "📞 Підтримка")
async def support(message: types.Message):

    await message.answer(
        "📞 Для допомоги зверніться до адміністратора. @adm_nexora_botforge"
    )



# ==========================
# ❓ Допомога
# ==========================

@router.message(F.text == "❓ Допомога")
async def help_menu(message: types.Message):

    await message.answer(
        """
❓ Допомога:

💼 Мої проєкти — ваші роботи
📤 Здати роботу — передати результат
💬 Чат — зв'язок з менеджером
📊 Статистика — ваші показники
"""
    )