from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from app.core.config import settings

class IsOwner(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        # Перевіряємо, чи збігається ID того, хто натиснув кнопку/написав повідомлення, з вашим ID з config.py
        return event.from_user.id == settings.OWNER_ID