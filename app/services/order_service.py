# services/order_service.py

class OrderService:
    @staticmethod
    async def create_order(user_id: int, product_name: str):
        # Тут буде логіка роботи з БД або Google Sheets
        # Наприклад: запис у базу даних
        return f"Замовлення на '{product_name}' для користувача {user_id} успішно створено!"

    @staticmethod
    async def get_order_status(order_id: int):
        # Логіка перевірки статусу
        return {"id": order_id, "status": "В обробці"}