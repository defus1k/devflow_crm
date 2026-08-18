from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from app.core.logger import logger
from app.db.session import async_session
from app.models.log import SystemLog

class LoggingMiddleware(BaseMiddleware):
    """
    Middleware для логування всіх вхідних повідомлень.
    """
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        # Логуємо інформацію про користувача та його запит
        if isinstance(event, Message) and event.from_user:
            user_info = f"User {event.from_user.id} ({event.from_user.username})"
            text = event.text or "Not a text message"
            logger.info(f"Вхідний запит: {user_info} | Текст: {text}")

        try:
            return await handler(event, data)
        except Exception as e:
            # Якщо хендлер викликав помилку, ми логуємо її тут
            logger.error(f"Помилка при обробці запиту: {e}", exc_info=True)
            raise e