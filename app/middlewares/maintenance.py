from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from app.core.config import settings

class MaintenanceMiddleware(BaseMiddleware):
    """
    Middleware для режиму технічних робіт.
    Якщо в налаштуваннях встановлено прапорець, блокує всі запити.
    """
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        # Перевіряємо прапорець у конфігурації
        if settings.IS_MAINTENANCE_MODE:
            if isinstance(event, Message):
                await event.answer(
                    "⚙️ **Технічні роботи**\n\n"
                    "Ми оновлюємо систему для покращення роботи. Будь ласка, спробуйте пізніше."
                )
            # Зупиняємо виконання будь-якого іншого хендлера
            return

        return await handler(event, data)