from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from cachetools import TTLCache


class AntiFloodMiddleware(BaseMiddleware):
    """Простий middleware для захисту від флуду."""

    def __init__(self, limit: int = 3, ttl_seconds: int = 2):
        self.limit = limit
        self.ttl_seconds = ttl_seconds
        self.cache = TTLCache(maxsize=10000, ttl=ttl_seconds)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
            current = self.cache.get(user_id, 0)
            if current >= self.limit:
                await event.answer("⏳ Занадто часто надсилаєте повідомлення. Зачекайте трохи.")
                return None
            self.cache[user_id] = current + 1
        return await handler(event, data)