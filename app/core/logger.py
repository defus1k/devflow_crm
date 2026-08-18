import sys
from loguru import logger
from pathlib import Path
from app.core.config import settings

# Створюємо папку для логів, якщо вона не існує
log_path = Path("logs")
log_path.mkdir(exist_ok=True)

# Очищаємо стандартні налаштування логера
logger.remove()

# 1. Лог в консоль (для зручного дебагу)
logger.add(
    sys.stderr,
    level=settings.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True,
    backtrace=False,
    diagnose=False,
)

# 2. Лог у файл (історія всіх подій системи)
# rotation="10 MB" — файл буде оновлюватися, коли виросте до 10 МБ
# retention="10 days" — зберігаємо історію за останні 10 днів
logger.add(
    "logs/devflow.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    enqueue=True # Важливо для асинхронності, щоб не блокувати головний потік
)

# 3. Окремий лог для критичних помилок
logger.add(
    "logs/errors.log",
    level="ERROR",
    rotation="100 MB",
    enqueue=True
)

__all__ = ["logger"]