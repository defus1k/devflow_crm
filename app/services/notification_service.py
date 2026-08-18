# services/notification_service.py
from aiogram import Bot

class NotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_order_confirmation(self, user_id: int, order_info: str):
        """Надсилає підтвердження клієнту."""
        message = f"✅ Ваше замовлення прийнято!\nІнфо: {order_info}"
        await self.bot.send_message(chat_id=user_id, text=message)

    async def notify_admin(self, message_text: str):
        """Сповіщення для адмінів про важливі події."""
        ADMIN_ID = 123456789  # Краще брати з конфігу
        await self.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 [ADMIN]: {message_text}")

    async def send_reminder(self, user_id: int, text: str):
        """Надсилає нагадування про оплату або терміни."""
        await self.bot.send_message(chat_id=user_id, text=f"⏰ Нагадування: {text}")