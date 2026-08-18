import os
import subprocess
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.config import settings
from app.core.logger import logger

async def run_database_backup():
    """
    Фонова задача: створення дампу бази даних PostgreSQL.
    """
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{backup_dir}/backup_{timestamp}.sql"
    
    # Команда для вивантаження бази даних
    # Примітка: переконайтеся, що .pgpass налаштовано або PGPASSWORD встановлено в середовищі
    cmd = [
        "pg_dump",
        "-h", settings.DB_HOST,
        "-U", settings.DB_USER,
        "-f", filename,
        settings.DB_NAME
    ]
    
    try:
        logger.info(f"Початок резервного копіювання: {filename}")
        subprocess.run(cmd, check=True, env={**os.environ, "PGPASSWORD": settings.DB_PASSWORD.get_secret_value()})
        logger.info(f"Бекап успішно збережено у {filename}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Помилка створення бекапу: {e}")

def setup_backup_scheduler(scheduler: AsyncIOScheduler):
    """
    Реєстрація задачі: автоматичний бекап щодня о 03:00 ночі.
    """
    scheduler.add_job(
        run_database_backup, 
        'cron', 
        hour=3, 
        minute=0
    )