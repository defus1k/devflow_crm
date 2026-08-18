import aiohttp
from app.core.config import settings
from app.core.logger import logger

class DiscordService:
    """
    Сервіс для надсилання повідомлень у канали Discord через Webhooks.
    """
    def __init__(self):
        self.webhook_url = settings.DISCORD_WEBHOOK_URL

    async def send_notification(self, title: str, description: str, color: int = 0x00ff00):
        """
        Надсилає повідомлення у форматі Embed у канал Discord.
        """
        if not self.webhook_url:
            return

        async with aiohttp.ClientSession() as session:
            payload = {
                "embeds": [{
                    "title": title,
                    "description": description,
                    "color": color
                }]
            }
            try:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status != 204:
                        logger.error(f"Помилка відправки в Discord: {await response.text()}")
            except Exception as e:
                logger.error(f"Виняток при роботі з Discord: {e}")