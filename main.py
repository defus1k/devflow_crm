import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Імпорти ваших модулів
from app.core.config import settings
from app.handlers import setup_routers

# Налаштування логування для відстеження роботи бота
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main() -> None:
    """
    Основна функція запуску бота.
    """
    # Ініціалізація бота з використанням вашого токена
    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    # Диспетчер для обробки подій
    dp = Dispatcher()

    # Підключення всіх роутерів через вашу функцію setup_routers
    setup_routers(dp)

    # Видаляємо старі оновлення (повідомлення), які прийшли, поки бот був вимкнений
    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("========================================")
    logger.info("🚀 Nexora BotForge успішно запущений")
    logger.info("========================================")

    try:
        # Запуск бота в режимі опитування (polling)
        await dp.start_polling(bot)
    finally:
        # Коректне закриття сесії бота при зупинці
        await bot.session.close()
        logger.info("Бот зупинений.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Запуск зупинений користувачем (Ctrl+C).")