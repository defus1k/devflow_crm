from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.order import Order
from sqlalchemy import select, and_

router = Router()

@router.callback_query(F.data == "owner_payments")
async def show_pending_payments(callback: types.CallbackQuery):
    async with async_session() as session:
        # Шукаємо замовлення, які завершені, але ще не оплачені розробнику
        query = select(Order).where(Order.status == "completed")
        result = await session.execute(query)
        pending = result.scalars().all()

    if not pending:
        await callback.message.edit_text("✅ Всі виплати здійснені. Черга порожня.")
        return

    builder = InlineKeyboardBuilder()
    for order in pending:
        builder.button(text=f"💸 {order.budget} USD | Замовлення #{order.id}", callback_data=f"pay_confirm_{order.id}")
    builder.adjust(1)
    
    await callback.message.edit_text("⏳ **Черга на виплату:**", reply_markup=builder.as_markup())

@router.callback_query(F.data == "owner_fin_approve_payouts")
async def show_pending_payments_from_finance(callback: types.CallbackQuery):
    await show_pending_payments(callback)


@router.callback_query(F.data.startswith("pay_confirm_"))
async def confirm_payment(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_")[2])
    
    async with async_session() as session:
        order = await session.get(Order, order_id)
        if order:
            await session.commit()
            await callback.message.answer(f"✅ Виплату за замовлення #{order_id} підтверджено!")
            
    await callback.answer()