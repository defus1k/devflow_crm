from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select, func
from app.db.session import async_session
from app.models.order import Order
from app.models.ticket import Ticket

router = Router()

# Описуємо стани для введення запитання у підтримку
class SupportState(StatesGroup):
    waiting_for_question = State()


@router.message(Command("manager_dashboard"))
@router.message(F.text == "💼 Панель менеджера")
async def manager_dashboard(message: types.Message):
    """
    Виводить розширену статистику та панель управління для менеджера.
    """
    manager_id = message.from_user.id

    async with async_session() as session:
        # Статистика конкретно для цього менеджера (за user_id)
        total_orders = await session.scalar(
            select(func.count(Order.id)).where(Order.user_id == manager_id)
        ) or 0
        
        # Передано в ІТ
        sent_to_it = await session.scalar(
            select(func.count(Order.id)).where(
                Order.user_id == manager_id,
                Order.status.in_(["in_work", "revision", "completed"])
            )
        ) or 0

        # Завершені замовлення
        completed_orders = await session.scalar(
            select(func.count(Order.id)).where(
                Order.user_id == manager_id,
                Order.status == "completed"
            )
        ) or 0

        # Відкриті тікети підтримки
        open_tickets = await session.scalar(
            select(func.count(Ticket.id)).where(Ticket.status == "open")
        ) or 0

    builder = InlineKeyboardBuilder()
    builder.button(text="📦 Мої активні замовлення", callback_data="manager_my_orders")
    builder.button(text="📊 Детальна статистика", callback_data="manager_stats_detail")
    builder.button(text=f"💬 Тікети підтримки ({open_tickets})", callback_data="manage_tickets")
    builder.adjust(1)
    
    dashboard_text = (
        "📊 <b>Особистий кабінет менеджера</b>\n\n"
        f"📌 Всього створено замовлень: <b>{total_orders}</b>\n"
        f"🚀 Передано в ІТ-відділ: <b>{sent_to_it}</b>\n"
        f"✅ Успішно завершено: <b>{completed_orders}</b>\n"
        f"💬 Відкритих тікетів у системі: <b>{open_tickets}</b>\n\n"
        "Виберіть необхідний розділ нижче:"
    )

    await message.answer(dashboard_text, reply_markup=builder.as_markup(), parse_mode="HTML")


@router.callback_query(F.data == "manager_stats_detail")
async def manager_stats_detail(callback: types.CallbackQuery):
    manager_id = callback.from_user.id

    async with async_session() as session:
        total_orders = await session.scalar(
            select(func.count(Order.id)).where(Order.user_id == manager_id)
        ) or 0
        completed_orders = await session.scalar(
            select(func.count(Order.id)).where(
                Order.user_id == manager_id,
                Order.status == "completed"
            )
        ) or 0
        in_work_orders = await session.scalar(
            select(func.count(Order.id)).where(
                Order.user_id == manager_id,
                Order.status == "in_work"
            )
        ) or 0

    text = (
        "📈 <b>Детальна статистика роботи</b>\n\n"
        f"• Оброблено клієнтів / замовлень: <b>{total_orders}</b>\n"
        f"• Зараз в роботі у розробників: <b>{in_work_orders}</b>\n"
        f"• Закритих успішних проєктів: <b>{completed_orders}</b>\n"
        "• <i>Для отримання розширеного фінансового звіту зверніться до адміністратора.</i>"
    )

    kb = InlineKeyboardBuilder()
    kb.button(text="🔙 Назад до панелі", callback_data="back_to_dashboard")
    
    await callback.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "back_to_dashboard")
async def back_to_dashboard(callback: types.CallbackQuery):
    manager_id = callback.from_user.id
    async with async_session() as session:
        total_orders = await session.scalar(select(func.count(Order.id)).where(Order.user_id == manager_id)) or 0
        sent_to_it = await session.scalar(select(func.count(Order.id)).where(Order.user_id == manager_id, Order.status.in_(["in_work", "revision", "completed"]))) or 0
        completed_orders = await session.scalar(select(func.count(Order.id)).where(Order.user_id == manager_id, Order.status == "completed")) or 0
        open_tickets = await session.scalar(select(func.count(Ticket.id)).where(Ticket.status == "open")) or 0

    builder = InlineKeyboardBuilder()
    builder.button(text="📦 Мої активні замовлення", callback_data="manager_my_orders")
    builder.button(text="📊 Детальна статистика", callback_data="manager_stats_detail")
    builder.button(text=f"💬 Тікети підтримки ({open_tickets})", callback_data="manage_tickets")
    builder.adjust(1)
    
    dashboard_text = (
        "📊 <b>Особистий кабінет менеджера</b>\n\n"
        f"📌 Всього створено замовлень: <b>{total_orders}</b>\n"
        f"🚀 Передано в ІТ-відділ: <b>{sent_to_it}</b>\n"
        f"✅ Успішно завершено: <b>{completed_orders}</b>\n"
        f"💬 Відкритих тікетів у системі: <b>{open_tickets}</b>\n\n"
        "Виберіть необхідний розділ нижче:"
    )

    await callback.message.edit_text(dashboard_text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


# --- ОБРОБНИК ТІКЕТІВ / ПІДТРИМКИ ---

@router.callback_query(F.data == "manage_tickets")
async def ask_support_question(callback: types.CallbackQuery, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.button(text="❌ Скасувати", callback_data="cancel_support")
    
    await callback.message.edit_text(
    "💬 <b>Центр підтримки</b>\n\n"
    "Напишіть ваше питання нижче у чат з будь-яких питань.\n\n"

    "💬 <b>Також ви завжди можете звернутися безпосередньо до нашої команди:</b>\n\n"

    "👑 <b>@defus1k</b> — <i>Головний засновник та керівник проєкту Nexora BotForge.</i>\n\n"

    "📋 <b>@nameobizateln0</b> — <i>Керівник менеджерського відділу. "
    "Допоможе з питаннями щодо замовлень, менеджерів та організації роботи.</i>",
    reply_markup=kb.as_markup(),
    parse_mode="HTML"
)
    await state.set_state(SupportState.waiting_for_question)
    await callback.answer()


@router.message(SupportState.waiting_for_question)
async def process_user_question(message: types.Message, state: FSMContext):
    user = message.from_user
    user_identifier = f"@{user.username}" if user.username else f"<a href='tg://user?id={user.id}'>{user.full_name}</a>"
    question_text = message.text

    # Текст сповіщення із зазначенням вашого контакту
    text_to_admin = (
        "📩 <b>Нове звернення / питання!</b>\n\n"
        f"👤 Від: {user_identifier} (ID: <code>{user.id}</code>)\n"
        f"💬 Питання: {question_text}\n\n"
        "Контакт для зв'язку: @adm_nexora_botforge"
    )

    # Тут можна надіслати це повідомлення куди потрібно (наприклад, у чат адміністраторам або назад)
    await message.answer("✅ Ваше питання успішно надіслано! Менеджер зв'яжеться з вами найближчим часом.\nКонтакт для зв'язку: <b>@adm_nexora_botforge</b>", parse_mode="HTML")
    await state.clear()


@router.callback_query(F.data == "cancel_support", SupportState.waiting_for_question)
async def cancel_support_process(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Скасовано.")
    await callback.answer()