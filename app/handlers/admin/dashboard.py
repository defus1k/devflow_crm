from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select, func

from app.db.session import async_session
from app.models.order import Order
from app.models.application import Application
from app.models.user import User
from app.models.ticket import Ticket
from app.keyboards.admin.dashboard import get_admin_dashboard_kb

router = Router()


def _get_admin_return_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад до панелі", callback_data="admin_panel")
    builder.adjust(1)
    return builder


async def _build_admin_panel_text() -> tuple[str, int, int, int]:
    async with async_session() as session:
        pending_apps = await session.scalar(select(func.count(Application.id))) or 0
        active_orders = await session.scalar(select(func.count(Order.id)).where(Order.status == 'in_progress')) or 0
        total_users = await session.scalar(select(func.count(User.telegram_id))) or 0
    return (
        "🛡 <b>Панель адміністратора</b>\n"
        f"📊 Заявки: {pending_apps}\n"
        f"📦 Активні замовлення: {active_orders}\n"
        f"👥 Користувачі: {total_users}",
        pending_apps,
        active_orders,
        total_users,
    )


# 1. Головна кнопка адміна (Reply)
@router.message(F.text == "🛡 Панель адміна")
async def open_admin_panel(message: types.Message):
    panel_text, pending_apps, active_orders, _ = await _build_admin_panel_text()
    await message.answer(
        panel_text,
        reply_markup=get_admin_dashboard_kb(
            pending_applications=pending_apps,
            active_orders=active_orders,
        ),
        parse_mode="HTML",
    )


# 2. Обробка кнопок дашборду (Callback)
@router.callback_query(F.data == "admin_panel")
async def open_admin_panel_from_callback(callback: CallbackQuery):
    panel_text, pending_apps, active_orders, _ = await _build_admin_panel_text()
    await callback.message.edit_text(
        panel_text,
        reply_markup=get_admin_dashboard_kb(
            pending_applications=pending_apps,
            active_orders=active_orders,
        ),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin_apps")
async def show_apps(callback: CallbackQuery):
    async with async_session() as session:
        applications = (
            (await session.execute(select(Application).order_by(Application.id.desc()).limit(10)))
            .scalars()
            .all()
        )

        if not applications:
            text = "📥 <b>Нові заявки:</b>\nПоки що немає жодної заявки."
        else:
            lines = ["📥 <b>Останні заявки:</b>"]
            for app in applications:
                user = await session.get(User, app.user_id)
                user_name = user.full_name if user else "Невідомий"
                lines.append(
                    f"#{app.id} | {app.topic} | {app.status} | {user_name}"
                )
            text = "\n".join(lines)

    await callback.message.edit_text(
        text,
        reply_markup=_get_admin_return_kb().as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin_orders")
async def show_orders(callback: CallbackQuery):
    async with async_session() as session:
        orders = (
            (await session.execute(select(Order).order_by(Order.created_at.desc()).limit(10)))
            .scalars()
            .all()
        )

        if not orders:
            text = "📦 <b>Керування замовленнями:</b>\nНемає замовлень."
        else:
            lines = ["📦 <b>Останні замовлення:</b>"]
            for order in orders:
                lines.append(
                    f"#{order.id} | {order.title} | {order.status} | ₴{order.budget} | клієнт {order.user_id}"
                )
            text = "\n".join(lines)

    await callback.message.edit_text(
        text,
        reply_markup=_get_admin_return_kb().as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin_staff_list")
async def show_staff_list(callback: CallbackQuery):
    async with async_session() as session:
        staff = (
            (await session.execute(
                select(User).where(User.role.in_(["manager", "developer", "admin", "owner"])).order_by(User.role.asc(), User.full_name.asc())
            ))
            .scalars()
            .all()
        )

        if not staff:
            text = "👥 <b>Персонал:</b>\nНемає зареєстрованих співробітників."
        else:
            lines = ["👥 <b>Персонал:</b>"]
            for user in staff:
                lines.append(f"• {user.full_name} | {user.role} | @{user.username or '—'}")
            text = "\n".join(lines)

    await callback.message.edit_text(
        text,
        reply_markup=_get_admin_return_kb().as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin_urgent_support")
async def show_urgent_support(callback: CallbackQuery):
    async with async_session() as session:
        tickets = (
            (await session.execute(
                select(Ticket)
                .where(Ticket.status.in_(["open", "in_progress"]))
                .order_by(Ticket.priority.desc(), Ticket.created_at.desc())
                .limit(10)
            ))
            .scalars()
            .all()
        )

        if not tickets:
            text = "🚨 <b>Термінові питання:</b>\nНаразі немає відкритих звернень."
        else:
            lines = ["🚨 <b>Термінові питання:</b>"]
            for ticket in tickets:
                user = await session.get(User, ticket.user_id)
                user_name = user.full_name if user else str(ticket.user_id)
                lines.append(
                    f"#{ticket.id} | {ticket.subject} | {ticket.status} | {ticket.priority} | {user_name}"
                )
            text = "\n".join(lines)

    await callback.message.edit_text(
        text,
        reply_markup=_get_admin_return_kb().as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "main_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("🔙 Повернуто до головного меню.")
    await callback.answer()