from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select

from app.keyboards.client.review import get_review_kb
from app.db.session import async_session
from app.models.order import Order
from app.models.user import User
from app.models.balance import Balance
from app.core.config import settings as config
from app.keyboards.client.menu import get_main_menu_kb
from app.keyboards.client.payment import get_payment_kb 
from app.services.balance_service import calculate_balance_after_debit, validate_balance_change
from app.services.security_service import validate_uploaded_file
from app.states.payment import PaymentStates

router = Router()

class OrderForm(StatesGroup):
    project_type = State()
    title = State()
    description = State()
    budget = State()
    contact = State()

class PaymentState(StatesGroup):
    waiting_for_amount = State()

class AdminPaymentState(StatesGroup):
    waiting_for_amount = State()

class ReviewState(StatesGroup):
    waiting_for_review = State()

# --- КНОПКИ ---
def get_confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Підтвердити", callback_data="confirm_order")],
        [InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_order")]
    ])

def get_take_order_kb(order_id: int, client_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Взяти в роботу", callback_data=f"take_order:{order_id}:{client_id}")]
    ])

def get_manager_billing_kb(order_id: int, client_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Надіслати рахунок", callback_data=f"send_bill:{order_id}:{client_id}")],
        [InlineKeyboardButton(text="✅ Завершити замовлення", callback_data=f"complete_order:{order_id}:{client_id}")]
    ])

def get_finance_approve_kb(client_id: int, order_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Зарахувати оплату", callback_data=f"ask_amount:{client_id}:{order_id}")]
    ])

# --- ЛОГІКА ОПИТУВАННЯ (ФОРМА ЗАМОВЛЕННЯ) ---
@router.message(OrderForm.project_type)
async def set_type(message: types.Message, state: FSMContext):
    await state.update_data(project_type=message.text)
    await message.answer("🔥 Введіть назву проекту:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderForm.title)

@router.message(OrderForm.title)
async def set_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("📝 Опишіть проект:")
    await state.set_state(OrderForm.description)

@router.message(OrderForm.description)
async def set_desc(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("💰 Вкажіть бюджет (тільки число грн):")
    await state.set_state(OrderForm.budget)

@router.message(OrderForm.budget)
async def set_budget(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❌ Введіть коректне число:")
    await state.update_data(budget=int(message.text))
    await message.answer("📞 Вкажіть ваші контакти для зв'язку (телеграм або номер):")
    await state.set_state(OrderForm.contact)

@router.message(OrderForm.contact)
async def set_contacts(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    data = await state.get_data()
    text = (
        f"📋 <b>Перевірте замовлення:</b>\n\n"
        f"🛠 <b>Тип:</b> {data['project_type']}\n"
        f"📌 <b>Назва:</b> {data['title']}\n"
        f"📝 <b>Опис:</b> {data['description']}\n"
        f"💰 <b>Бюджет:</b> {data['budget']} грн\n"
        f"📞 <b>Контакти:</b> {data['contact']}"
    )
    await message.answer(text, reply_markup=get_confirm_kb(), parse_mode="HTML")

# --- ОБРОБКА ЗАМОВЛЕННЯ ---
@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    topic = await bot.create_forum_topic(chat_id=config.CLIENT_FOR_ID if hasattr(config, 'CLIENT_FOR_ID') else config.CLIENT_FORUM_ID, name=f"Замовлення {data['title']}")
    thread_id = topic.message_thread_id
    
    async with async_session() as session:
        order = Order(user_id=callback.from_user.id, **data, status="pending", thread_id=thread_id)
        session.add(order)
        await session.commit()
        await session.refresh(order)
    
    await bot.edit_forum_topic(chat_id=config.CLIENT_FORUM_ID, message_thread_id=thread_id, name=f"Замовлення №{order.id}")
    
    text = (
        f"🆕 <b>Нове замовлення №{order.id}</b>\n\n"
        f"👤 <b>Клієнт:</b> @{callback.from_user.username or 'без нікнейму'}\n"
        f"🛠 <b>Тип:</b> {data['project_type']}\n"
        f"📌 <b>Назва:</b> {data['title']}\n"
        f"📝 <b>Опис:</b> {data['description']}\n"
        f"💰 <b>Бюджет:</b> {data['budget']} грн\n"
        f"📞 <b>Контакти:</b> {data['contact']}"
    )
    
    await bot.send_message(
        chat_id=config.CLIENT_FORUM_ID,
        message_thread_id=thread_id,
        text=text,
        reply_markup=get_take_order_kb(order.id, callback.from_user.id),
        parse_mode="HTML"
    )
    
    await state.clear()
    await callback.answer("✅ Замовлення створено!")
    
    # Редагуємо поточне повідомлення на успіх і виводимо меню
    await callback.message.delete()

    await callback.message.answer(
        f"✅ <b>Замовлення №{order.id} успішно створено!</b>\n\n"
        "🏠 Повертаємось у головне меню:",
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("take_order:"))
async def take_order_callback(callback: types.CallbackQuery):
    parts = callback.data.split(":")
    if len(parts) < 3:
        await callback.answer("Помилка: неповні дані замовлення!", show_alert=True)
        return
    _, order_id, client_id = parts[:3]
    
    async with async_session() as session:
        order = await session.get(Order, int(order_id))
        if order:
            order.status = "in_work"
            await session.commit()
    await callback.message.edit_text(
        text=callback.message.text + f"\n\n✅ Взяв в роботу: {callback.from_user.full_name}", 
        reply_markup=get_manager_billing_kb(int(order_id), int(client_id)), 
        parse_mode="HTML"
    )
    await callback.answer("Ви взяли замовлення!")

@router.callback_query(F.data.startswith("complete_order:"))
async def complete_order(callback: types.CallbackQuery, bot: Bot):
    parts = callback.data.split(":")
    if len(parts) < 3:
        await callback.answer("Помилка: неповні дані замовлення!", show_alert=True)
        return
    _, order_id, client_id = parts[:3]
    
    async with async_session() as session:
        order = await session.get(Order, int(order_id))
        if order:
            order.status = "completed"

            balance_record = await session.execute(select(Balance).where(Balance.user_id == int(client_id)))
            balance_obj = balance_record.scalar_one_or_none()

            if balance_obj is None:
                balance_obj = Balance(user_id=int(client_id), amount=0)
                session.add(balance_obj)

            new_balance = calculate_balance_after_debit(balance_obj.amount, order.budget)
            balance_obj.amount = new_balance
            await session.commit()
            await bot.edit_forum_topic(chat_id=config.CLIENT_FORUM_ID, message_thread_id=order.thread_id)

    await bot.send_message(
        int(client_id),
        f"🎉 Ваше замовлення успішно виконано!\n\n💳 З вашого балансу списано {float(order.budget or 0):.2f} грн.\nЗалишок: {float(balance_obj.amount if 'balance_obj' in locals() else 0):.2f} грн",
        reply_markup=get_review_kb(int(order_id)),
    )
    await callback.message.edit_text(text=callback.message.text + "\n\n🏁 Завершено.", reply_markup=None)

@router.callback_query(F.data.startswith("send_bill:"))
async def start_billing(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split(":")
    if len(parts) < 3:
        await callback.answer("Помилка: неповні дані замовлення!", show_alert=True)
        return
    _, order_id, client_id = parts[:3]
    
    await state.update_data(order_id=order_id, client_id=client_id)
    await state.set_state(PaymentState.waiting_for_amount)
    await callback.message.answer("💰 Введіть суму оплати:")

@router.message(PaymentState.waiting_for_amount)
async def process_amount(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if not message.text.isdigit():
        return await message.answer("❌ Введіть коректну суму (тільки цифри):")

    await bot.send_message(
        chat_id=int(data['client_id']), 
        text=f"💳 Рахунок на оплату: {message.text} грн.", 
        reply_markup=get_payment_kb(int(data['order_id']), int(message.text))
    )
    await message.answer(f"✅ Рахунок на {message.text} грн надіслано клієнту!")
    await state.clear()

@router.callback_query(F.data.startswith("confirm_pay_"))
async def handle_client_payment_click(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    order_id = int(parts[2])
    amount = int(parts[3])

    await state.set_state(PaymentStates.waiting_for_screenshot)
    await state.update_data(
        order_id=order_id,
        amount=amount
    )

    await callback.message.answer(
        f"💳 <b>Оплата замовлення на суму: {amount} грн</b>\n\n"
        "💳 <b>Реквізити для оплати:</b>\n"
        "<code>4149 4990 7597 0887</code> (Приватбанк, Руслан С.)\n\n"
        "📸 Будь ласка, надішліть сюди скріншот оплати з вашого банківського додатка.",
        parse_mode="HTML"
    )
    await callback.answer()

# --- ФІНАНСИ: СКРІНШОТ ВІД КЛІЄНТА ТА ПЕРЕСИЛАННЯ АДМІНУ ---
@router.message(PaymentStates.waiting_for_screenshot, F.photo)
async def handle_payment_photo(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    order_id = data.get("order_id")
    amount = data.get("amount")

    photo_id = message.photo[-1].file_id
    file_info = await bot.get_file(photo_id)
    
    if not validate_uploaded_file("payment.jpg", "image/jpeg", int(file_info.file_size or 0)):
        await message.answer("❌ Неможливо прийняти файл: недопустимий тип або розмір.")
        return

    await bot.send_photo(
        chat_id=config.FINANCE_FORUM_ID,
        photo=photo_id,
        caption=(
            f"📸 <b>Оплата від клієнта @{message.from_user.username or 'без ніку'}</b>\n"
            f"🆔 ID користувача: {message.from_user.id}\n"
            f"📦 Замовлення: #{order_id}\n"
            f"💰 Сума до зарахування: {amount} грн"
        ),
        reply_markup=get_finance_approve_kb(message.from_user.id, order_id),
        parse_mode="HTML"
    )

    await message.answer("✅ Скріншот отримано! Адміністратор перевірить його найближчим часом.")
    await state.clear()

@router.callback_query(F.data.startswith("ask_amount:"))
async def ask_amount(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split(":")
    client_id = parts[1]
    order_id = parts[2] if len(parts) > 2 else "0"
    
    await state.update_data(client_id=client_id, order_id=order_id)
    await state.set_state(AdminPaymentState.waiting_for_amount)
    await callback.message.answer("💰 Введіть точну суму для зарахування на баланс:")
    await callback.answer()

@router.message(AdminPaymentState.waiting_for_amount)
async def process_admin_amount(message: types.Message, state: FSMContext, bot: Bot):
    if not message.text.isdigit():
        return await message.answer("❌ Введіть число!")
    
    amount = int(message.text)
    validate_balance_change(amount)
    data = await state.get_data()
    client_id = int(data['client_id'])
    order_id = data.get('order_id', '0')

    async with async_session() as session:
        res = await session.execute(select(Balance).where(Balance.user_id == client_id))
        bal_record = res.scalar_one_or_none()
        
        if bal_record:
            bal_record.amount += amount
            await session.commit()
            updated_balance = bal_record.amount
        else:
            new_bal = Balance(user_id=client_id, amount=amount)
            session.add(new_bal)
            await session.commit()
            updated_balance = amount

    # Зворотний зв'язок адміністратору в чат
    await message.answer(f"✅ Баланс користувача `{client_id}` успішно поповнено на `{amount} грн`. Новий баланс: `{updated_balance} грн`", parse_mode="HTML")

    # Зворотний зв'язок КЛІЄНТУ в особисті повідомлення
    try:
        await bot.send_message(
            chat_id=client_id,
            text=(
                f"🎉 <b>Баланс успішно поповнено!</b>\n\n"
                f"💳 Платіж за замовлення #{order_id} на суму <b>{amount} грн</b> підтверджено адміністратором.\n"
                f"💰 Ваш поточний баланс: <b>{updated_balance:.2f} грн</b>"
            ),
            parse_mode="HTML",
            reply_markup=get_main_menu_kb()
        )
    except Exception as e:
        await message.answer(f"⚠️ Не вдалося надіслати сповіщення клієнту в ЛС: {e}")

    await state.clear()

# --- НАЗАД ТА СКАСУВАННЯ ---
@router.callback_query(F.data.startswith("client_order_view_"))
async def handle_back(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("🏠 Головне меню:", reply_markup=get_main_menu_kb())
    await callback.answer("Повернення...")

@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await callback.message.delete()

        await callback.message.answer(
            "❌ Замовлення скасовано.\n\n🏠 Головне меню:",
            reply_markup=get_main_menu_kb()
        )

    except Exception:
        await callback.message.answer(
            "❌ Замовлення скасовано.\n\n🏠 Головне меню:",
            reply_markup=get_main_menu_kb()
        )
        await callback.answer("Скасовано")

@router.callback_query(F.data.startswith("review_rate_"))
async def process_rating(callback: types.CallbackQuery, state: FSMContext):
    _, _, order_id, star = callback.data.split("_")
    await state.update_data(order_id=order_id, rating=star)
    await callback.message.edit_text("⭐️ Ви обрали " + star + " зірок. Напишіть коментар:")
    await state.set_state(ReviewState.waiting_for_review)

@router.message(ReviewState.waiting_for_review)
async def process_review(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.send_message(config.REVIEWS_FORUM_ID, f"⭐️ Відгук №{data['order_id']}: {data['rating']} зірок\nКоментар: {message.text}")
    await message.answer("✅ Дякуємо за ваш відгук!", reply_markup=get_main_menu_kb())
    await state.clear()