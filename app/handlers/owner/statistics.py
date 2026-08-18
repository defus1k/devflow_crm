from aiogram import Router, F, types
from sqlalchemy import select, func
from app.db.session import async_session
from app.models.user import User
# Якщо у тебе є модель замовлень (Orders), імпортуй її теж:
# from app.models.order import Order 

router = Router()

@router.message(F.text == "📊 Глобальні звіти")
async def global_reports(message: types.Message):
    async with async_session() as session:
        # Приклад: рахуємо кількість користувачів
        total_users = await session.scalar(select(func.count()).select_from(User))
        
        # Приклад: рахуємо скільки людей не клієнти (працівники)
        staff_count = await session.scalar(select(func.count()).select_from(User).where(User.role != "client"))
        
        # Тут ти можеш додати запити до таблиці замовлень, наприклад:
        # total_orders = await session.scalar(select(func.count()).select_from(Order))

    await message.answer(
        f"📊 <b>Глобальна статистика:</b>\n\n"
        f"👥 Всього користувачів: <code>{total_users}</code>\n"
        f"🛠 Працівників у системі: <code>{staff_count}</code>\n"
        # f"📦 Всього замовлень: <code>{total_orders}</code>\n"
        f"\n<i>Дані оновлено в реальному часі.</i>",
        parse_mode="HTML"
    )