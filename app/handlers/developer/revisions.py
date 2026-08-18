from aiogram import Router, types, F
from app.db.session import async_session
from app.models.order import Order
from sqlalchemy import select

router = Router()

@router.callback_query(F.data.startswith("dev_view_revision_"))
async def view_revision_notes(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_")[3])
    
    async with async_session() as session:
        order = await session.get(Order, order_id)
        
        # Виводимо коментарі менеджера
        await callback.message.answer(
            f"⚠️ **Необхідні правки для #{order.id}**\n\n"
            f"Коментар менеджера: {order.revision_notes or 'Без коментарів'}\n\n"
            "Виправте зауваження та натисніть 'Здати роботу повторно'."
        )
    await callback.answer()