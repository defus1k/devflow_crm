from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, TelegramObject
from aiogram.types import Message


class SecurityMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("user")
        if event is not None and isinstance(event, Message):
            if not getattr(event.from_user, "id", None):
                await event.answer("❌ Сесія недійсна.")
                return
        if user is None:
            if isinstance(event, Message):
                await event.answer("❌ Потрібна авторизація.")
            return
        return await handler(event, data)
