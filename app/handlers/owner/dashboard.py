from aiogram import Router, F, types
from aiogram.filters import Command, CommandObject
from sqlalchemy import select, func
import logging
import datetime

from app.db.session import async_session
from app.models.user import User
from app.models.order import Order
from app.models.application import Application
from app.keyboards.owner import get_owner_dashboard_kb
from app.models.payment import Payment
from app.models.review import Review
from app.models.ticket import Ticket

router = Router()
MY_TELEGRAM_ID = 1268981313

# --- ЛОГІКА ---

async def list_staff_logic(message: types.Message):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.role != "client"))
        staff = result.scalars().all()
        
        if not staff:
            await message.answer("🛠 Працівників поки немає.")
            return

        text = "👥 <b>Список персоналу:</b>\n\n"
        for u in staff:
            text += f"👤 {u.full_name} | ID: <code>{u.telegram_id}</code> | Роль: <code>{u.role}</code>\n"
        
        await message.answer(text, parse_mode="HTML")

# --- ОБРОБНИКИ (Reply та Inline) ---

@router.message(F.text == "👑 Панель власника")
async def owner_panel_reply(message: types.Message):
    async with async_session() as session:
        count_workers = await session.scalar(
            select(func.count()).select_from(User).where(User.role != "client")
        )
    await message.answer(
        "👑 <b>Панель власника</b>\nОберіть розділ:",
        reply_markup=get_owner_dashboard_kb(active_orders=0, total_profit=0.0, staff_online=count_workers or 0),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "owner_panel")
async def owner_panel_callback(callback: types.CallbackQuery):
    await callback.answer()
    async with async_session() as session:
        count_workers = await session.scalar(
            select(func.count()).select_from(User).where(User.role != "client")
        )
        active_orders = await session.scalar(select(func.count(Order.id)).where(Order.status == "in_progress")) or 0
        total_profit = await session.scalar(select(func.coalesce(func.sum(Order.budget), 0)).where(Order.status == "completed")) or 0
    await callback.message.edit_text(
        "👑 <b>Панель власника</b>\nОберіть розділ:",
        reply_markup=get_owner_dashboard_kb(active_orders=int(active_orders), total_profit=float(total_profit), staff_online=int(count_workers or 0)),
        parse_mode="HTML"
    )

@router.message(F.text == "👥 Управління персоналом")
async def staff_reply(message: types.Message):
    await list_staff_logic(message)

@router.callback_query(F.data == "owner_employees_list")
async def staff_callback(callback: types.CallbackQuery):
    await callback.answer()
    await list_staff_logic(callback.message)

@router.message(F.text == "📊 Глобальні звіти")
async def get_global_stats(message: types.Message):
    if message.from_user.id != MY_TELEGRAM_ID: return

    async with async_session() as session:
        try:
            count_users = await session.scalar(select(func.count(User.telegram_id))) or 0
            count_apps = await session.scalar(select(func.count(Application.id))) or 0
            total_orders = await session.scalar(select(func.count(Order.id))) or 0
            completed_orders = await session.scalar(select(func.count(Order.id)).where(Order.status == 'completed')) or 0
            total_earnings = await session.scalar(select(func.sum(Order.budget)).where(Order.status == 'completed')) or 0
            
            stats_text = (
                f"📊 <b>Глобальна статистика Nexora BotForge</b>\n\n"
                f"👥 Всього користувачів: <b>{count_users}</b>\n"
                f"📥 Активних заявок: <b>{count_apps}</b>\n\n"
                f"🚀 Всього замовлень: <b>{total_orders}</b>\n"
                f"✅ Виконано проектів: <b>{completed_orders}</b>\n"
                f"💰 Загальний дохід: <b>{float(total_earnings or 0):.2f} грн</b>\n\n"
                f"📈 <i>Оновлено: {datetime.datetime.now().strftime('%H:%M:%S')}</i>"
            )
            await message.answer(stats_text, parse_mode="HTML")
            
        except Exception as e:
            logging.error(f"Помилка stats: {e}")
            await message.answer("❌ Помилка при зверненні до БД. Перевір, чи існує таблиця orders.")

@router.callback_query(F.data == "owner_orders_report")
async def owner_orders_report(callback: types.CallbackQuery):
    async with async_session() as session:
        active_orders = await session.scalar(select(func.count(Order.id)).where(Order.status == "in_progress")) or 0
        completed_orders = await session.scalar(select(func.count(Order.id)).where(Order.status == "completed")) or 0
        pending_orders = await session.scalar(select(func.count(Order.id)).where(Order.status == "new")) or 0

    text = (
        "📦 <b>Статус замовлень</b>\n"
        f"🟢 В роботі: {active_orders}\n"
        f"✅ Виконано: {completed_orders}\n"
        f"🕒 Нові: {pending_orders}"
    )
    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "owner_finance_report")
async def owner_finance_report(callback: types.CallbackQuery):
    async with async_session() as session:
        total_profit = await session.scalar(select(func.coalesce(func.sum(Order.budget), 0)).where(Order.status == "completed")) or 0
        payments_pending = await session.scalar(select(func.count(Payment.id)).where(Payment.status == "pending")) or 0
        payments_success = await session.scalar(select(func.count(Payment.id)).where(Payment.status == "success")) or 0

    text = (
        "💰 <b>Фінансова сводка</b>\n"
        f"✅ Виплачено/зараховано: {float(total_profit):.2f} грн\n"
        f"⏳ Очікує оплат: {payments_pending}\n"
        f"✔️ Успішних платежів: {payments_success}"
    )
    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "owner_staff_report")
async def owner_staff_report(callback: types.CallbackQuery):
    async with async_session() as session:
        count_staff = await session.scalar(select(func.count(User.telegram_id)).where(User.role != "client")) or 0
        count_reviews = await session.scalar(select(func.count(Review.id))) or 0
        count_tickets = await session.scalar(select(func.count(Ticket.id)).where(Ticket.status.in_(["open", "in_progress"]))) or 0

    text = (
        "👥 <b>Команда і операції</b>\n"
        f"🧑‍💼 Співробітників: {count_staff}\n"
        f"⭐ Відгуків: {count_reviews}\n"
        f"🎫 Відкритих звернень: {count_tickets}"
    )
    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()


@router.message(F.text.in_(["💳 Фінанси", "👤 Особистий кабінет", "📞 Контакти"]))
async def handle_menus(message: types.Message):
    # 1. Обробка фінансів
    if message.text == "💳 Фінанси":
        if message.from_user.id != MY_TELEGRAM_ID:
            await message.answer("❌ У вас немає доступу до фінансів.")
            return

        async with async_session() as session:
            total_earnings = await session.scalar(
                select(func.sum(Order.budget)).where(Order.status == 'completed')
            ) or 0
            
            await message.answer(
                f"💰 <b>Фінансова аналітика:</b>\n\n"
                f"Загальний заробіток: <b>{float(total_earnings):.2f} грн</b>",
                parse_mode="HTML"
            )

    # 2. Обробка інших кнопок
    elif message.text == "👤 Особистий кабінет":
        await message.answer("👤 Ваш особистий кабінет.")
        
    elif message.text == "📞 Контакти":
        await message.answer("📞 Контакти власника та підтримки.")
# --- КОМАНДИ ---

@router.message(Command("find"))
async def find_user(message: types.Message, command: CommandObject):
    if not command.args:
        await message.answer("❌ Введіть: /find @username")
        return
    
    username = command.args.replace("@", "")
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.username == username))
        if user:
            await message.answer(f"🔎 Знайдено: {user.full_name}\n🆔 ID: <code>{user.telegram_id}</code>\n🛡 Роль: <code>{user.role}</code>", parse_mode="HTML")
        else:
            await message.answer("❌ Користувача не знайдено.")

@router.message(Command("setrole"))
async def set_role(message: types.Message, command: CommandObject):
    if not command.args or len(command.args.split()) < 2:
        await message.answer("❌ Формат: /setrole [ID] [роль]")
        return
    
    args = command.args.split()
    try:
        target_id = int(args[0])
        new_role = args[1]
    except ValueError:
        await message.answer("❌ ID має бути числом.")
        return

    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == target_id))
        if user:
            user.role = new_role
            await session.commit()
            await message.answer(f"✅ Роль для {target_id} змінена на {new_role}")
        else:
            await message.answer("❌ Користувача не знайдено.")


@router.message(Command("owner_stats"))
async def owner_stats_command(message: types.Message):
    async with async_session() as session:
        count_users = await session.scalar(select(func.count(User.telegram_id))) or 0
        count_staff = await session.scalar(select(func.count(User.telegram_id)).where(User.role != "client")) or 0
        count_orders = await session.scalar(select(func.count(Order.id))) or 0
        completed_orders = await session.scalar(select(func.count(Order.id)).where(Order.status == "completed")) or 0
        total_profit = await session.scalar(select(func.coalesce(func.sum(Order.budget), 0)).where(Order.status == "completed")) or 0

    await message.answer(
        "📊 <b>Операційна сводка власника</b>\n"
        f"👥 Користувачів: {count_users}\n"
        f"🧑‍💼 Співробітників: {count_staff}\n"
        f"📦 Замовлень: {count_orders}\n"
        f"✅ Виконано: {completed_orders}\n"
        f"💰 Дохід: {float(total_profit):.2f} грн",
        parse_mode="HTML",
    )