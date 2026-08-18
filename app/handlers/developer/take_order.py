from aiogram import Router, types, F, Bot
from sqlalchemy import select

from app.db.session import async_session
from app.models.order import Order
from app.models.user import User
from app.services.forum_service import build_manager_accept_message, build_developer_accept_message, build_contact_keyboard

router = Router()


@router.callback_query(F.data.startswith("dev_take_"))
async def accept_order(callback: types.CallbackQuery, bot: Bot):
    order_id = int(callback.data.split("_")[2])
    dev_id = callback.from_user.id

    async with async_session() as session:
        order = await session.get(Order, order_id)
        if not order:
            await callback.answer("❌ Замовлення не знайдено.", show_alert=True)
            return

        if order.developer_id is not None or order.status in {"in_progress", "completed", "closed"}:
            await callback.message.answer("❌ Це замовлення вже не доступне для прийому.")
            await callback.answer()
            return

        order.developer_id = dev_id
        order.status = "in_progress"
        if order.manager_id:
            manager = await session.get(User, order.manager_id)
            developer = await session.get(User, dev_id)
            if manager and developer:
                await bot.send_message(
                    order.manager_id,
                    build_manager_accept_message(developer),
                    reply_markup=build_contact_keyboard(dev_id, "💬 Написать разработчику"),
                )
                await bot.send_message(
                    dev_id,
                    build_developer_accept_message(manager),
                    reply_markup=build_contact_keyboard(order.manager_id, "💬 Написать менеджеру"),
                )
        await session.commit()

    await callback.message.answer(f"✅ Ви успішно прийняли замовлення #{order_id}.")
    await callback.answer()