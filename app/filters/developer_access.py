from aiogram import types
from aiogram.dispatcher.flags import FlagDecorator
from aiogram import Router


class DeveloperAccessFilter:
    async def __call__(self, callback: types.CallbackQuery) -> bool:
        from app.models.user import User
        from app.db.session import async_session
        from sqlalchemy import select

        async with async_session() as session:
            result = await session.execute(select(User).where(User.telegram_id == callback.from_user.id))
            user = result.scalar_one_or_none()
        return bool(user and user.role == "developer")
