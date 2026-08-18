from decimal import Decimal
from aiogram import F, Router, types, Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select, func
from app.models.user import User
from app.models.balance import Balance
from app.models.order import Order
from app.db.session import async_session
from app.keyboards.client.profile import get_profile_kb

router = Router()

# Твій ID форуму
SUPPORT_FORUM_ID = -1004344291921

class ProfileStates(StatesGroup):
    waiting_for_new_name = State()

class WithdrawState(StatesGroup):
    waiting_for_amount = State()
    waiting_for_details = State()

# СТАНИ ДЛЯ ДОРАБОТКИ/ВИПРАВЛЕННЯ ЗАМОВЛЕННЯ КОРИСТУВАЧЕМ
class OrderRevisionState(StatesGroup):
    waiting_for_revision_comment = State()

# 1. ОБРОБКА КНОПКИ ПРОФІЛЮ
@router.message(F.text == "👤 Особистий кабінет")
async def show_profile(message: types.Message):
    async with async_session() as session:
        user_res = await session.execute(select(User).filter(User.telegram_id == message.from_user.id))
        user = user_res.scalar_one_or_none()
        
        bal_res = await session.execute(select(Balance).filter(Balance.user_id == message.from_user.id))
        balance_obj = bal_res.scalar_one_or_none()
        
        balance_amount = balance_obj.amount if balance_obj else 0.0
        
        profile_text = (
            f"👤 <b>Ваш особистий профіль</b>\n\n"
            f"🆔 ID: {user.telegram_id}\n"
            f"👤 Ім'я: {user.full_name}\n"
            f"💰 Баланс: {balance_amount} грн\n"
            f"📅 Дата реєстрації: {user.created_at.strftime('%d.%m.%Y')}"
        )
        await message.answer(profile_text, parse_mode="HTML", reply_markup=get_profile_kb())

# 2. СТАТИСТИКА ТА СПИСОК ЗАМОВЛЕНЬ З ІНФОЮ
@router.callback_query(F.data == "profile_stats")
async def stats_handler(callback: CallbackQuery):
    async with async_session() as session:
        res_count = await session.execute(select(func.count(Order.id)).filter(Order.user_id == callback.from_user.id))
        count = res_count.scalar()
        
        # Отримуємо всі замовлення користувача для розширеної інфи
        orders_res = await session.execute(
            select(Order).filter(Order.user_id == callback.from_user.id).order_by(Order.created_at.desc())
        )
        orders = orders_res.scalars().all()
        
        res_last = await session.execute(select(Order.created_at).filter(Order.user_id == callback.from_user.id).order_by(Order.created_at.desc()))
        last_date = res_last.scalar()
        date_str = last_date.strftime('%d.%m.%Y') if last_date else "Немає"

        orders_buttons = []
        for order in orders:
            # Можна виводити назву замовлення або ID + статус
            status_emoji = {
                "pending": "⏳",
                "in_work": "🛠",
                "completed": "✅",
                "revision": "🔄"
            }.get(order.status, "📦")
            
            orders_buttons.append([
                InlineKeyboardButton(
                    text=f"{status_emoji} Замовлення #{order.id}", 
                    callback_data=f"user_order_detail:{order.id}"
                )
            ])
        
        # Додаємо кнопку повернення в меню у кінець
        orders_buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")])

        orders_kb = InlineKeyboardMarkup(inline_keyboard=orders_buttons)

        await callback.message.edit_text(
            f"📊 <b>Ваша статистика та замовлення:</b>\n\n"
            f"📦 Всього замовлень: {count}\n"
            f"🕒 Останнє замовлення: {date_str}\n\n"
            f"👇 <i>Натисніть на замовлення нижче, щоб переглянути деталі, статус та надіслати на доопрацювання:</i>",
            parse_mode="HTML",
            reply_markup=orders_kb
        )
    await callback.answer()

# ДЕТАЛІ ОКРЕМОГО ЗАМОВЛЕННЯ ДЛЯ КОРИСТУВАЧА (СТАТУС + КНОПКА ДОРАБОТАТИ)
@router.callback_query(F.data.startswith("user_order_detail:"))
async def user_order_detail_handler(callback: CallbackQuery):
    order_id = int(callback.data.split(":")[1])
    
    async with async_session() as session:
        res = await session.execute(select(Order).filter(Order.id == order_id, Order.user_id == callback.from_user.id))
        order = res.scalar_one_or_none()
        
        if not order:
            return await callback.answer("❌ Замовлення не знайдено!", show_alert=True)
            
        status_names = {
            "pending": "⏳ В очікуванні",
            "in_work": "🛠 В роботі",
            "completed": "✅ Виконано",
            "revision": "🔄 На доопрацюванні"
        }
        current_status_name = status_names.get(order.status, order.status)
        
        text = (
            f"📦 <b>Деталі замовлення #{order.id}</b>\n\n"
            f"📌 Статус: <b>{current_status_name}</b>\n"
            f"📅 Створено: {order.created_at.strftime('%d.%m.%Y о %H:%M')}\n"
            f"📝 Опис / Деталі: {getattr(order, 'description', 'Не вказано')}\n"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Доопрацювати / Виправити", callback_data=f"order_revision:{order.id}")],
            [InlineKeyboardButton(text="◀️ До списку замовлень", callback_data="profile_stats")]
        ])
        
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)
        await callback.answer()

# ПОЧАТОК ПРОЦЕСУ ДОРАБОТКИ ЗАМОВЛЕННЯ
@router.callback_query(F.data.startswith("order_revision:"))
async def start_order_revision(callback: CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split(":")[1])
    await state.update_data(revision_order_id=order_id)
    await state.set_state(OrderRevisionState.waiting_for_revision_comment)
    
    await callback.message.answer("✍️ Введіть детально, що саме потрібно доопрацювати або виправити в цьому замовленні:")
    await callback.answer()

@router.message(OrderRevisionState.waiting_for_revision_comment)
async def process_order_revision_comment(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    order_id = data.get("revision_order_id")
    user_id = message.from_user.id
    comment = message.text
    
    async with async_session() as session:
        res = await session.execute(select(Order).filter(Order.id == order_id))
        order = res.scalar_one_or_none()
        if order:
            order.status = "revision"
            await session.commit()
            
    # Надсилаємо сповіщення в підтримку / форум для айтишника
    try:
        await bot.send_message(
            chat_id=SUPPORT_FORUM_ID,
            text=(f"🔄 <b>ЗАПИТ НА ДООПРАЦЮВАННЯ ЗАМОВЛЕННЯ</b>\n\n"
                  f"📦 Замовлення ID: #{order_id}\n"
                  f"👤 Клієнт: @{message.from_user.username or 'без ніку'} (ID: {user_id})\n"
                  f"💬 Коментар клієнта: {comment}"),
            parse_mode="HTML"
        )
    except Exception:
        pass
        
    await message.answer("✅ Ваші побажання щодо доопрацювання надіслано адміністраторам/розробнику!")
    await state.clear()

# АДМІНСЬКИЙ КОМАНДНИЙ ІНТЕРФЕЙС ДЛЯ ЗМІНИ СТАТУСУ (ДЛЯ АЙТИШНИКА)
@router.message(F.text.startswith("/setstatus "))
async def admin_set_order_status(message: types.Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        return await message.answer("❌ Формат команди:\n`/setstatus [ID_замовлення] [статус]`\n\nДоступні статуси: `pending`, `in_work`, `completed`, `revision`", parse_mode="Markdown")
    
    try:
        order_id = int(parts[1])
    except ValueError:
        return await message.answer("❌ ID замовлення має бути числом!")
        
    new_status = parts[2].strip()
    allowed_statuses = ["pending", "in_work", "completed", "revision"]
    
    if new_status not in allowed_statuses:
        return await message.answer(f"❌ Невірний статус! Доступні: {', '.join(allowed_statuses)}")
        
    async with async_session() as session:
        res = await session.execute(select(Order).filter(Order.id == order_id))
        order = res.scalar_one_or_none()
        
        if not order:
            return await message.answer("❌ Замовлення не знайдено в базі даних!")
            
        order.status = new_status
        await session.commit()
        
        await message.answer(f"✅ Статус замовлення #{order_id} успішно змінено на <b>{new_status}</b>!", parse_mode="HTML")

# 3. ЗМІНА ІМЕНІ
@router.callback_query(F.data == "profile_edit")
async def edit_name_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✍️ Введіть ваше нове ім'я:")
    await state.set_state(ProfileStates.waiting_for_new_name)
    await callback.answer()

@router.message(ProfileStates.waiting_for_new_name)
async def process_new_name(message: types.Message, state: FSMContext):
    async with async_session() as session:
        res = await session.execute(select(User).filter(User.telegram_id == message.from_user.id))
        user = res.scalar_one_or_none()
        if user:
            user.full_name = message.text
            await session.commit()
    await message.answer(f"✅ Ім'я успішно змінено на: {message.text}")
    await state.clear()

# 4. ВИВІД КОШТІВ
@router.callback_query(F.data == "profile_withdraw")
async def start_withdraw(callback: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        res = await session.execute(
            select(Order).filter(Order.user_id == callback.from_user.id, Order.status.in_(["pending", "in_work"]))
        )
        if res.scalars().first():
            return await callback.answer("❌ У вас є активні замовлення, вивід заблоковано!", show_alert=True)
            
    await state.set_state(WithdrawState.waiting_for_amount)
    await callback.message.answer("💰 Введіть суму, яку бажаєте вивести:")
    await callback.answer()

@router.message(WithdrawState.waiting_for_amount)
async def process_withdraw_amount(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❌ Введіть число!")
    await state.update_data(amount=message.text)
    await state.set_state(WithdrawState.waiting_for_details)
    await message.answer("💳 Введіть ваші реквізити для виводу:")

@router.message(WithdrawState.waiting_for_details)
async def process_withdraw_details(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    amount_to_withdraw = Decimal(data['amount'])
    user_id = message.from_user.id
    
    async with async_session() as session:
        res = await session.execute(select(Balance).filter(Balance.user_id == user_id))
        bal = res.scalar_one_or_none()
        
        if not bal or bal.amount < amount_to_withdraw:
            await message.answer("❌ Недостатньо коштів на балансі!")
            return await state.clear()

        await bot.send_message(
            chat_id=SUPPORT_FORUM_ID,
            text=(f"💸 <b>ЗАЯВКА НА ВИВІД</b>\n\n"
                  f"👤 Клієнт: @{message.from_user.username or 'без ніку'}\n"
                  f"🆔 ID: {user_id}\n"
                  f"💰 Сума: {amount_to_withdraw} грн\n"
                  f"💳 Реквізити: {message.text}"),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Виплачено", callback_data=f"payout_done:{user_id}:{amount_to_withdraw}")]
            ]),
            parse_mode="HTML"
        )
    await message.answer("✅ Заявку на вивід успішно відправлено адміністраторам!")
    await state.clear()

@router.callback_query(F.data.startswith("payout_done:"))
async def finish_payout(callback: CallbackQuery, bot: Bot):
    _, user_id, amount_str = callback.data.split(":")
    amount = Decimal(amount_str)
    
    async with async_session() as session:
        res = await session.execute(select(Balance).filter(Balance.user_id == int(user_id)))
        bal = res.scalar_one_or_none()
        if bal:
            bal.amount -= amount
            await session.commit()
            
    await callback.message.edit_text(text=callback.message.text + "\n\n✅ Статус: <b>Завершено</b>", parse_mode="HTML")
    try:
        await bot.send_message(int(user_id), f"💸 <b>Виплату успішно здійснено!</b>\n\nСума: {amount} грн.", parse_mode="HTML")
    except: pass
    await callback.answer("Баланс клієнта оновлено.")

@router.message(F.text.startswith("/check "))
async def admin_check_balance(message: types.Message):
    parts = message.text.split()
    if len(parts) < 2: return await message.answer("Вкажіть ID")
    target_id = int(parts[1])
    async with async_session() as session:
        res = await session.execute(select(Balance).filter(Balance.user_id == target_id))
        bal = res.scalar_one_or_none()
        if bal: await message.answer(f"💰 Баланс користувача {target_id}: {bal.amount} грн.")
        else: await message.answer("❌ Користувача не знайдено.")

# 5. НАЗАД
@router.callback_query(F.data == "main_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Повернення до меню")