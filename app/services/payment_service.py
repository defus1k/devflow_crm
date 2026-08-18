# services/payment_service.py

class PaymentService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def create_payment_link(self, amount: float, description: str):
        """
        Тут буде логіка звернення до платіжного шлюзу (Stripe, Mono, LiqPay).
        """
        # Емуляція звернення до зовнішнього API
        print(f"Генерація посилання на оплату: {amount} грн за '{description}'")
        
        # Наприклад, повертаємо фіктивне посилання
        return "https://payment.example.com/pay/123456"

    async def verify_payment(self, payment_id: str):
        """
        Перевірка статусу платежу через API.
        """
        # Логіка запиту до сервера платіжної системи
        return {"status": "success", "payment_id": payment_id}