from aiogram import Bot
from app.core.config import settings

class TelegramIntegration:
    """
    Клас для розширеної роботи з Telegram API.
    Дозволяє боту виконувати дії поза основним циклом обробки.
    """
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_to_channel(self, chat_id: int | str, text: str, photo: str = None):
        """
        Відправка повідомлень в окремий канал (наприклад, канал з логами замовлень).
        """
        try:
            if photo:
                return await self.bot.send_photo(chat_id, photo, caption=text)
            return await self.bot.send_message(chat_id, text)
        except Exception as e:
            # Логування помилки відправки
            return None

    async def forward_message(self, from_chat_id: int, message_id: int, to_chat_id: int):
        """
        Пересилання повідомлення від клієнта в адмінську групу.
        """
        return await self.bot.forward_message(to_chat_id, from_chat_id, message_id)