import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from app.core.config import settings
from app.core.logger import logger
from app.handlers import setup_routers # Ми створимо цей файл наступним

class DevFlowApplication:
    """
    Клас-фабрика для ініціалізації та запуску бота.
    """
    def __init__(self):
        self.bot = Bot(token=settings.BOT_TOKEN.get_secret_value())
        
        # Налаштування Redis для FSM (станів)
        self.redis = Redis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT, 
            db=settings.REDIS_DB
        )
        self.storage = RedisStorage(redis=self.redis)
        self.dp = Dispatcher(storage=self.storage)

    def setup_middleware(self):
        """
        Підключення Middleware (наприклад, для сесій БД).
        """
        # Тут ми додамо middleware для автоматичного прокидання сесії БД у кожен хендлер
        pass

    def setup_handlers(self):
        """Реєстрація всіх роутерів (хендлерів)."""
        self.dp.include_router(setup_routers())

    async def start(self):
        """Запуск бота."""
        try:
            logger.info("Запуск системи DevFlow CRM...")
            self.setup_handlers()
            self.setup_middleware()
            
            # Видалення вебхуків перед запуском (long polling)
            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.critical(f"Критична помилка при запуску: {e}")
        finally:
            await self.bot.session.close()
            await self.redis.close()

# Екземпляр застосунку
app = DevFlowApplication()