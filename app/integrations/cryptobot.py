import aiohttp
from app.core.config import settings

class CryptoBotAPI:
    """
    Сервіс для взаємодії з API CryptoBot (або CryptoPay).
    """
    def __init__(self):
        self.base_url = "https://pay.crypt.bot/api"
        self.headers = {
            "Crypto-Pay-API-Token": getattr(settings, "CRYPTOBOT_API_KEY", None) or getattr(settings, "CRYPTO_BOT_TOKEN", None)
        }

    async def create_invoice(self, amount: float, currency: str = "USDT"):
        """
        Створення рахунку на оплату.
        """
        async with aiohttp.ClientSession() as session:
            payload = {
                "asset": currency,
                "amount": str(amount),
                "description": "Оплата замовлення в CRM",
            }
            async with session.post(
                f"{self.base_url}/createInvoice", 
                json=payload, 
                headers=self.headers
            ) as response:
                data = await response.json()
                if data["ok"]:
                    return data["result"]
                return None

    async def check_invoice_status(self, invoice_id: int):
        """
        Перевірка, чи оплатив клієнт рахунок.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/getInvoices?invoice_ids={invoice_id}",
                headers=self.headers
            ) as response:
                data = await response.json()
                return data["result"]["items"][0] if data["ok"] else None