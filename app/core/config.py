import logging
import os
from typing import Literal
from pydantic import PostgresDsn, SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def validate_settings_payload(payload: dict, environment: str = "development") -> None:
    """Базовая валидация чувствительных значений перед запуском."""
    placeholder_values = {
        "BOT_TOKEN": {"your_bot_token_here", "replace_me", "token_here"},
        "JWT_SECRET": {"change_me_in_production", "replace_me", "jwt_secret"},
        "WEBHOOK_SECRET": {"change_me_in_production", "replace_me", "webhook_secret"},
    }

    if environment == "production":
        for key, forbidden in placeholder_values.items():
            value = payload.get(key)
            if isinstance(value, SecretStr):
                value = value.get_secret_value()
            if isinstance(value, str) and value.strip().lower() in forbidden:
                raise ValueError(f"{key} contains a placeholder value in production")

        db_url = payload.get("DATABASE_URL", "")
        if isinstance(db_url, str) and ("localhost" in db_url or "127.0.0.1" in db_url):
            raise ValueError("DATABASE_URL must not point to localhost in production")


class Settings(BaseSettings):
    """
    Централізований об'єкт конфігурації для всієї CRM.
    Використовує pydantic для валідації типів та значень.
    """
    
    # 1. Основні налаштування бота
    PROJECT_NAME: str = "Nexora BotForge"
    VERSION: str = "1.0.0"
    ENVIRONMENT: Literal["development", "production"] = "development"
    
    # 2. Telegram Bot Configuration
    BOT_TOKEN: SecretStr = Field(..., description="Токен бота від BotFather")
    OWNER_ID: int = Field(..., description="Telegram ID власника для доступу до CRM")
    # Telegram форуми
    CLIENT_FORUM_ID: int
    MANAGER_FORUM_ID: int
    DEVELOPER_FORUM_ID: int
    REVIEWS_FORUM_ID: int
    SUPPORT_FORUM_ID: int
    FINANCE_FORUM_ID: int
    DEVELOPER_ORDER_ID: int
    
    # 3. База даних (PostgreSQL)
    # Формат: postgresql+asyncpg://user:pass@host:port/dbname
    DATABASE_URL: PostgresDsn
    
    # 4. Redis (Кешування та FSM)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # 5. Безпека (JWT для API та Webhooks)
    JWT_SECRET: SecretStr = Field(..., description="Секретний ключ для підпису JWT")
    WEBHOOK_SECRET: str = Field(..., description="Токен для перевірки запитів від Webhook")
    
    # 6. Платіжні системи (API ключі для інтеграцій)
    CRYPTOBOT_API_KEY: str | None = None
    STRIPE_API_KEY: str | None = None
    
    # 7. Налаштування логування
    LOG_LEVEL: str = "INFO"

    # Конфігурація завантаження з файлу .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ігноруємо зайві змінні, якщо вони є в .env
    )

# Створення глобального об'єкта налаштувань
# Його можно импортировать в любом месте: from app.core.config import settings
settings = Settings()
validate_settings_payload(
    {
        "BOT_TOKEN": settings.BOT_TOKEN.get_secret_value() if hasattr(settings.BOT_TOKEN, "get_secret_value") else settings.BOT_TOKEN,
        "JWT_SECRET": settings.JWT_SECRET.get_secret_value() if hasattr(settings.JWT_SECRET, "get_secret_value") else settings.JWT_SECRET,
        "WEBHOOK_SECRET": settings.WEBHOOK_SECRET,
        "DATABASE_URL": str(settings.DATABASE_URL),
        "ENVIRONMENT": settings.ENVIRONMENT,
    },
    environment=settings.ENVIRONMENT,
)

# Ініціалізація логера, щоб він працював з першої секунди запуску
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("devflow")
logger.info(f"Конфігурацію {settings.PROJECT_NAME} успішно завантажено.")