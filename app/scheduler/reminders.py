from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order import Order, OrderStatus
from app.core.logger import logger
from datetime import datetime, timedelta

async def check_deadlines(session_factory):
    """
    Фонова задача: перевірка замовлень, де дедлайн вже близько.
    """
    logger.info("Запуск перевірки дедлайнів...")
    async with session_factory() as session:
        # Шукаємо замовлення в роботі, де дедлайн через 24 години або менше
        tomorrow = datetime.now() + timedelta(days=1)
        query = select(Order).where(
            Order.status == OrderStatus.IN_PROGRESS,
            Order.deadline <= tomorrow
        )
        result = await session.execute(query)
        orders = result.scalars().all()

        for order in orders:
            logger.info(f"Нагадування для замовлення {order.id}: дедлайн {order.deadline}")
            # Тут буде логіка відправки повідомлення в Telegram через бот
            # await bot.send_message(order.developer_id, f"Дедлайн для {order.title} завтра!")

def setup_reminders(scheduler: AsyncIOScheduler, session_factory):
    """
    Реєстрація задачі в планувальнику.
    """
    # Запускати перевірку щогодини
    scheduler.add_job(
        check_deadlines, 
        'interval', 
        hours=1, 
        args=[session_factory]
    )