from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.ticket import Ticket
from sqlalchemy import select, update

router = Router()

@router.callback_query(F.data == "admin_tickets")
async def show_tickets(callback: types.CallbackQuery):
    async with async_session() as session:
        # Отримуємо тільки відкриті тікети
        result = await session.execute(select(Ticket).where(Ticket.status == "open"))
        tickets = result.scalars().all()

    if not tickets:
        await callback.message.edit_text("✅ Всі тікети опрацьовано!")
        return

    builder = InlineKeyboardBuilder()
    for ticket in tickets:
        builder.button(text=f"🎫 Тікет #{ticket.id} | {ticket.user_name}", callback_data=f"admin_ticket_view_{ticket.id}")
    builder.adjust(1)
    
    await callback.message.edit_text("📩 **Відкриті тікети підтримки:**", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("admin_ticket_view_"))
async def view_ticket(callback: types.CallbackQuery):
    ticket_id = int(callback.data.split("_")[3])
    
    async with async_session() as session:
        ticket = await session.get(Ticket, ticket_id)
        
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Закрити тікет", callback_data=f"admin_ticket_close_{ticket_id}")
    builder.button(text="🔙 Назад", callback_data="admin_tickets")
    
    await callback.message.edit_text(
        f"📩 **Тікет #{ticket.id} від {ticket.user_name}**\n\n"
        f"Питання: {ticket.message}\n\n"
        "Ви можете відповісти користувачу через кнопку 'Відповісти' (реалізація через FSM).",
        reply_markup=builder.as_markup()
    )