import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.employee_service import EmployeeService
from app.services.notification_service import NotificationService
# Ми імпортуємо сервіси, які будуть виконувати реальну роботу

logger = logging.getLogger(__name__)

class SchedulerManager:
    """
    Клас для керування фоновими задачами CRM.
    """
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.employee_service = EmployeeService()
        self.notification_service = NotificationService()

    def setup_tasks(self):
        """
        Налаштування всіх періодичних задач.
        """
        # 1. Перевірка TikTok відео (кожні 6 годин)
        self.scheduler.add_job(
            self.employee_service.check_tiktok_compliance,
            trigger=CronTrigger(hour="*/6"),
            id="tiktok_check",
            replace_existing=True
        )

        # 2. Розрахунок KPI (щодня о 00:00)
        self.scheduler.add_job(
            self.employee_service.calculate_daily_kpi,
            trigger=CronTrigger(hour=0, minute=0),
            id="kpi_calc",
            replace_existing=True
        )

        # 3. Резервне копіювання БД (щодня о 03:00)
        self.scheduler.add_job(
            self.run_backup,
            trigger=CronTrigger(hour=3, minute=0),
            id="db_backup",
            replace_existing=True
        )

        logger.info("Всі фонові задачі налаштовані.")

    def start(self):
        self.scheduler.start()
        logger.info("Scheduler запущено.")

    async def run_backup(self):
        """Приклад методу для бекапу."""
        logger.info("Починається процес бекапу бази даних...")
        # Тут буде виклик утиліти pg_dump
        pass

# Створення екземпляра
scheduler_manager = SchedulerManager()