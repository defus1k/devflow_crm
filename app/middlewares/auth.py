from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repository.user_repository import UserRepository
from app.models.moderation import UserModeration
from app.models.log import SystemLog


class AuthMiddleware(BaseMiddleware):
    """Middleware для ідентифікації користувача та автоматичної реєстрації."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession = data.get("session")
        if session is None:
            return await handler(event, data)

        user_repo = UserRepository(session)
        from_user = getattr(event, "from_user", None)

        if from_user:
            user = await user_repo.get_by_telegram_id(from_user.id)
            if not user:
                user = await user_repo.create(
                    telegram_id=from_user.id,
                    username=from_user.username,
                    full_name=from_user.full_name,
                )
                await session.commit()
            data["user"] = user

        return await handler(event, data)