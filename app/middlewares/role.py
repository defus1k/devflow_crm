from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from app.models.user import UserRole

class RoleMiddleware(BaseMiddleware):
    """
    Middleware для перевірки прав доступу користувача.
    """
    def __init__(self, allowed_roles: list[UserRole] = None):
        self.allowed_roles = allowed_roles or []

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        # Отримуємо користувача, якого ми знайшли в AuthMiddleware
        user = data.get("user")
        
        # Якщо ми не задали обмеження, пропускаємо всіх
        if not self.allowed_roles:
            return await handler(event, data)
        
        # Перевірка ролі
        if user and user.role in self.allowed_roles:
            return await handler(event, data)
        
        # Якщо роль не підходить — блокуємо доступ
        if isinstance(event, Message):
            await event.answer("❌ У вас недостатньо прав для виконання цієї дії.")
        
        return # Зупиняємо виконання хендлера