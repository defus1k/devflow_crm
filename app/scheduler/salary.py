from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.order import Order, OrderStatus
from app.core.logger import logger
from datetime import datetime

async def calculate_monthly_salaries(session_factory):
    """
    Щомісячна задача: підрахунок виплат розробникам за завершені замовлення.
    """
    logger.info("Початок розрахунку зарплат...")
    async with session_factory() as session:
        # Агрегуємо суми замовлень по кожному розробнику за поточний місяць
        query = select(
            Order.developer_id, 
            func.sum(Order.budget).label("total_earnings")
        ).where(
            Order.status == OrderStatus.COMPLETED
        ).group_by(Order.developer_id)
        
        result = await session.execute(query)
        reports = result.all()

        for dev_id, total in reports:
            logger.info(f"Розробник {dev_id} заробив: {total}")
            # Тут можна інтегрувати логіку створення запиту на виплату (Payout)

def setup_salary_calculator(scheduler: AsyncIOScheduler, session_factory):
    """
    Реєстрація задачі в планувальнику (наприклад, 1-го числа кожного місяця).
    """
    scheduler.add_job(
        calculate_monthly_salaries, 
        'cron', 
        day=1, 
        hour=0, 
        args=[session_factory]
    )