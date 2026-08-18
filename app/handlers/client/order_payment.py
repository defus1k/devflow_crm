from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import update, delete

from app.core.config import settings
from app.db.session import async_session
from app.models.user import User
from app.models.order import Order
from app.states.payment import PaymentStates
from app.keyboards.client.payment import get_admin_payment_kb, get_confirm_cancel_kb
from app.keyboards.client.menu import get_main_menu_kb

router = Router()

# 1. Обробка натискання кнопки "Оплатити" -> Запит скріншота
# 1. Обробка натискання кнопки "Оплатити" -> Запит скріншота
@router.callback_query(F.data.startswith("confirm_pay_"))
async def ask_for_screenshot(callback: CallbackQuery, state: FSMContext):
    _, _, order_id, amount = callback.data.split("_")

    # На всякий случай очищаем старое состояние
    await state.clear()

    await state.set_state(PaymentStates.waiting_for_screenshot)
    await state.update_data(
        order_id=int(order_id),
        amount=int(amount)
    )

    await callback.message.answer(
        "💳 <b>Реквізити для оплати:</b>\n"
        "<code>4149 4990 7597 0887</code> (Приватбанк, Руслан С.)\n\n"
        "📸 Надішліть скріншот оплати.",
        parse_mode="HTML"
    )

    await callback.answer()


# 2. Обробка скріншота від клієнта

# 2. Обробка скріншота від клієнта

@router.message(PaymentStates.waiting_for_screenshot, F.photo)
async def process_screenshot(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()

    order_id = data["order_id"]
    amount = data["amount"]

    await bot.send_photo(
        chat_id=settings.FINANCE_FORUM_ID,
        photo=message.photo[-1].file_id,
        caption=(
            f"🔔 <b>Перевірка оплати!</b>\n"
            f"👤 Клієнт: {message.from_user.full_name}\n"
            f"📦 Замовлення: #{order_id}\n"
            f"💰 Сума: {amount} грн"
        ),
        parse_mode="HTML",
        reply_markup=get_admin_payment_kb(
            message.from_user.id,
            order_id,
            amount
        )
    )

    await message.answer(
        "✅ Скріншот надіслано!\n"
        "Очікуйте підтвердження адміністрацією."
    )

    # Перестаём ждать фото
    await state.clear()

# 3. Обробка натискання кнопки "Назад" (Попередження про скасування)
@router.callback_query(F.data.startswith("client_order_view_"))
async def ask_cancel_confirmation(callback: CallbackQuery):
    order_id = callback.data.split("_")[-1]
    await callback.message.edit_text(
        "⚠️ **Ви впевнені, що хочете скасувати замовлення?**\n"
        "Рахунок буде анульовано, а ви повернетесь у головне меню.",
        reply_markup=get_confirm_cancel_kb(int(order_id))
    )

# 4. Підтвердження скасування
@router.callback_query(F.data.startswith("confirm_cancel_"))
async def confirm_cancel(callback: CallbackQuery, state: FSMContext):
    order_id = callback.data.split("_")[-1]
    async with async_session() as session:
        await session.execute(delete(Order).where(Order.id == int(order_id)))
        await session.commit()
    
    await state.clear()
    await callback.message.edit_text(
        "❌ Замовлення було скасовано.\n🏠 Повернення до головного меню:", 
        reply_markup=get_main_menu_kb()
    )
    await callback.answer("Замовлення скасовано!")

# 5. Клієнт передумав скасовувати
@router.callback_query(F.data.startswith("resume_pay_"))
async def resume_payment(callback: CallbackQuery):
    # Просто видаляємо повідомлення з підтвердженням
    await callback.message.delete()
    await callback.answer("Продовжуємо!")

# 6. Адмін натискає "Зарахувати"
@router.callback_query(F.data.startswith("add_"))
async def approve_payment(callback: CallbackQuery, bot: Bot):
    _, user_id, order_id, amount = callback.data.split("_")
    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.telegram_id == int(user_id))
            .values(balance=User.balance + float(amount))
        )
        await session.commit()
    
    await callback.message.edit_caption(caption=f"✅ Зараховано {amount} грн користувачу {user_id}")
    await bot.send_message(
        chat_id=int(user_id), 
        text=f"🎉 **Баланс поповнено!**\nПлатіж за замовлення #{order_id} на суму {amount} грн успішно зараховано."
    )
    await callback.answer("Гроші зараховано!")

# 7. Адмін натискає "Відхилити"
@router.callback_query(F.data.startswith("reject_"))
async def reject_payment(callback: CallbackQuery):
    _, user_id, order_id = callback.data.split("_")
    await callback.message.edit_caption(caption="❌ Платіж відхилено адміністратором.")
    await callback.bot.send_message(int(user_id), f"⚠️ На жаль, платіж за замовлення #{order_id} було відхилено.")
    await callback.answer("Платіж відхилено")