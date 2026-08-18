from aiogram import Router, types, F
from app.db.session import async_session
from app.models.order import Order
from sqlalchemy import select

router = Router()

@router.callback_query(F.data.startswith("transfer_dev_"))
async def transfer_order(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_")[2])
    
    async with async_session() as session:
        order = await session.get(Order, order_id)
        
        # Перевірка: чи готове ТЗ (briefing_approved)
        if order and order.status == "briefing_approved":
            order.status = "in_progress"
            await session.commit()
            
            # Тут можна додати логіку відправки сповіщення розробнику (bot.send_message)
            await callback.message.answer(
                f"🚀 Замовлення #{order.id} успішно передано розробнику {order.developer_id}."
            )
        else:
            await callback.answer("Помилка: проект не пройшов брифування або вже в роботі.")
            
    await callback.answer()