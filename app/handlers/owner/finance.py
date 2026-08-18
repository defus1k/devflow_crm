from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from sqlalchemy import select, func, and_
from app.models.finance import Transaction
from app.models.order import Order
from app.models.payment import Payment
from app.keyboards.owner.finance import get_owner_finance_kb
from datetime import datetime, timedelta

router = Router()
ALLOWED_IDS = [1268981313] # Твій ID


def build_owner_finance_text(total_profit: float, pending_orders: int, payments_pending: int, payments_success: int) -> str:
    return (
        "📈 <b>Фінанси та виплати</b>\n\n"
        f"💰 Загальний прибуток: <b>{float(total_profit):.2f} грн</b>\n"
        f"📦 Очікують виплат: <b>{pending_orders} замовлень</b>\n"
        f"⏳ Очікує оплат: <b>{payments_pending}</b>\n"
        f"✅ Успішних платежів: <b>{payments_success}</b>"
    )


@router.callback_query(F.data == "owner_finance_manage")
async def owner_finance_manage(callback: types.CallbackQuery):
    await callback.answer()

    async with async_session() as session:
        total_profit = await session.scalar(
            select(func.coalesce(func.sum(Order.budget), 0)).where(Order.status == "completed")
        ) or 0
        pending_payout_amount = await session.scalar(
            select(func.coalesce(func.sum(Order.budget), 0)).where(Order.status == "completed")
        ) or 0
        pending_orders = await session.scalar(
            select(func.count(Order.id)).where(Order.status == "completed")
        ) or 0
        payments_pending = await session.scalar(select(func.count(Payment.id)).where(Payment.status == "pending")) or 0
        payments_success = await session.scalar(select(func.count(Payment.id)).where(Payment.status == "success")) or 0

    text = build_owner_finance_text(float(total_profit), int(pending_orders), int(payments_pending), int(payments_success))
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_owner_finance_kb(float(total_profit), float(pending_payout_amount)),
    )


@router.callback_query(F.data == "owner_fin_total")
async def owner_fin_total(callback: types.CallbackQuery):
    await callback.answer()

    async with async_session() as session:
        total_profit = await session.scalar(
            select(func.coalesce(func.sum(Order.budget), 0)).where(Order.status == "completed")
        ) or 0
        pending_payout_amount = await session.scalar(
            select(func.coalesce(func.sum(Order.budget), 0)).where(Order.status == "completed")
        ) or 0

    await callback.message.edit_text(
        f"💰 <b>Загальний прибуток</b>\n\n✅ Всього: <b>{float(total_profit):.2f} грн</b>\n⏳ Очікує виплат: <b>{float(pending_payout_amount):.2f} грн</b>",
        parse_mode="HTML",
    )


@router.callback_query(F.data == "owner_fin_pending")
async def owner_fin_pending(callback: types.CallbackQuery):
    await callback.answer()

    async with async_session() as session:
        pending_orders = await session.execute(
            select(Order).where(Order.status == "completed")
        )
        orders = pending_orders.scalars().all()

    if not orders:
        await callback.message.edit_text("✅ Немає замовлень, які очікують виплат.")
        return

    builder = InlineKeyboardBuilder()
    for order in orders:
        builder.button(text=f"🧾 Замовлення #{order.id} — {float(order.budget or 0):.2f} грн", callback_data=f"pay_confirm_{order.id}")
    builder.adjust(1)

    await callback.message.edit_text(
        "⏳ <b>Замовлення, що очікують виплати</b>",
        parse_mode="HTML",
        reply_markup=builder.as_markup(),
    )


@router.callback_query(F.data == "owner_fin_history")
async def owner_fin_history(callback: types.CallbackQuery):
    await callback.answer()

    async with async_session() as session:
        payments = await session.execute(
            select(Payment).order_by(Payment.created_at.desc()).limit(10)
        )
        items = payments.scalars().all()

    if not items:
        await callback.message.edit_text("🧾 Історія транзакцій порожня.")
        return

    lines = ["🧾 <b>Останні транзакції</b>"]
    for payment in items:
        created = payment.created_at.strftime("%d.%m.%Y %H:%M") if payment.created_at else "—"
        lines.append(f"• #{payment.id} | {float(payment.amount or 0):.2f} грн | {payment.status} | {created}")

    await callback.message.edit_text("\n".join(lines), parse_mode="HTML")


@router.callback_query(F.data == "owner_fin_report")
async def owner_fin_report(callback: types.CallbackQuery):
    await callback.answer()

    async with async_session() as session:
        today = datetime.utcnow().date()
        month_start = datetime.utcnow().replace(day=1).date()

        total_completed = await session.scalar(
            select(func.coalesce(func.sum(Order.budget), 0)).where(Order.status == "completed")
        ) or 0
        today_revenue = await session.scalar(
            select(func.coalesce(func.sum(Order.budget), 0)).where(
                and_(Order.status == "completed", func.date(Order.created_at) == today)
            )
        ) or 0
        month_revenue = await session.scalar(
            select(func.coalesce(func.sum(Order.budget), 0)).where(
                and_(Order.status == "completed", func.date(Order.created_at) >= month_start)
            )
        ) or 0

    text = (
        "📈 <b>Звіт за період</b>\n\n"
        f"💰 Всього завершених: <b>{float(total_completed):.2f} грн</b>\n"
        f"📅 За сьогодні: <b>{float(today_revenue):.2f} грн</b>\n"
        f"🗓️ За цей місяць: <b>{float(month_revenue):.2f} грн</b>"
    )
    await callback.message.edit_text(text, parse_mode="HTML")


@router.message(Command("finance"))
async def finance_stats(message: types.Message):
    if message.from_user.id not in ALLOWED_IDS:
        return

    async with async_session() as session:
        # 1. Загальна сума (Revenue)
        total_revenue = await session.scalar(select(func.sum(Transaction.amount))) or 0
        
        # 2. Кількість замовлень
        total_orders = await session.scalar(select(func.count(Transaction.id))) or 0
        
        # 3. Середній чек
        avg_check = total_revenue / total_orders if total_orders > 0 else 0
        
        # 4. Дохід за сьогодні (для динаміки)
        today = datetime.utcnow().date()
        today_revenue = await session.scalar(
            select(func.sum(Transaction.amount)).where(func.date(Transaction.created_at) == today)
        ) or 0

        # Формування звіту
        report = (
            f"📊 <b>Фінансовий звіт</b>\n\n"
            f"💰 <b>Загальний оборот:</b> <code>{total_revenue:,.2f} грн</code>\n"
            f"📦 <b>Всього замовлень:</b> <code>{total_orders}</code>\n"
            f"💵 <b>Середній чек:</b> <code>{avg_check:,.2f} грн</code>\n"
            f"⚡️ <b>За сьогодні:</b> <code>{today_revenue:,.2f} грн</code>\n\n"
            f"📈 <i>Дані оновлено: {datetime.now().strftime('%H:%M:%S')}</i>"
        )
        
        await message.answer(report, parse_mode="HTML")