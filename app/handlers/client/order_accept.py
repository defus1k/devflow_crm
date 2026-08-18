from aiogram import Router, F
from aiogram.types import CallbackQuery

from sqlalchemy import select

from app.db.session import async_session
from app.models.order import Order

from app.services.forum_service import ForumService


router = Router()


@router.callback_query(
    F.data.startswith("order_confirm_")
)
async def accept_order(
    callback: CallbackQuery
):

    # получаем ID заказа
    order_id = int(
        callback.data.split("_")[2]
    )


    async with async_session() as session:


        result = await session.execute(
            select(Order)
            .where(Order.id == order_id)
        )


        order = result.scalar_one_or_none()


        if order is None:

            await callback.answer(
                "❌ Замовлення не знайдено",
                show_alert=True
            )

            return



        # меняем статус
        order.status = "confirmed"


        await session.commit()



        # отправляем в форум менеджеров

        forum = ForumService(
            db_session=session,
            bot=callback.bot
        )


        await forum.create_order_topic(
            order_id=order.id,
            title=order.title,
            username=(
                callback.from_user.username
                or "Без username"
            ),
            description=order.description,
            budget=order.budget
        )



    await callback.message.edit_text(
        """
✅ <b>Замовлення підтверджено!</b>


🚀 Заявка передана менеджеру.

Очікуйте відповіді.
        """,
        parse_mode="HTML"
    )


    await callback.answer()



@router.callback_query(
    F.data.startswith("order_edit_")
)
async def edit_order(
    callback: CallbackQuery
):

    await callback.answer(
        "✏️ Редагування замовлення буде доступне скоро"
    )



@router.callback_query(
    F.data == "main_menu"
)
async def cancel_order(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        """
❌ Замовлення скасовано.
"""
    )


    await callback.answer()