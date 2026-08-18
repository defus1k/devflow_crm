import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from app.models.order import Order, OrderStatus
from app.core.logger import logger

async def check_tiktok_video_status(session_factory):
    """
    Фонова задача: перевірка статусу відео або охоплень через TikTok API.
    """
    logger.info("Початок перевірки активності TikTok посилань...")
    
    async with session_factory() as session:
        # Шукаємо замовлення, які очікують підтвердження публікації в TikTok
        query = select(Order).where(Order.status == OrderStatus.IN_PROGRESS)
        result = await session.execute(query)
        orders = result.scalars().all()

        for order in orders:
            if order.task_link and "tiktok.com" in order.task_link:
                try:
                    # Імітація запиту до API або парсингу
                    async with aiohttp.ClientSession() as client:
                        async with client.get(order.task_link) as response:
                            if response.status == 200:
                                logger.info(f"Відео {order.id} доступне та успішно перевірено.")
                                # Тут можна додати логіку оновлення статусу замовлення
                except Exception as e:
                    logger.error(f"Помилка перевірки TikTok для замовлення {order.id}: {e}")

def setup_tiktok_checker(scheduler: AsyncIOScheduler, session_factory):
    """
    Реєстрація задачі: перевірка кожні 6 годин.
    """
    scheduler.add_job(
        check_tiktok_video_status, 
        'interval', 
        hours=6, 
        args=[session_factory]
    )