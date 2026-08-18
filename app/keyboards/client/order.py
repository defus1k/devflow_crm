from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_order_details_kb(order_id: int, status: str) -> InlineKeyboardMarkup:
    """
    Клавіатура детального перегляду замовлення.
    :param order_id: ID замовлення.
    :param status: Поточний статус (pending, paid, completed, cancelled).
    """
    builder = InlineKeyboardBuilder()
    
    # Кнопки залежно від статусу
    if status == "pending":
        builder.button(text="💳 Оплатити", callback_data=f"order_pay_{order_id}")
        builder.button(text="❌ Скасувати", callback_data=f"order_cancel_{order_id}")
        
    elif status == "completed":
        builder.button(text="⭐ Залишити відгук", callback_data=f"order_review_{order_id}")
        builder.button(text="📂 Завантажити результат", callback_data=f"order_download_{order_id}")
        
    # Кнопка повернення до списку замовлень
    builder.button(text="🔙 До списку замовлень", callback_data="client_orders")
    
    # Налаштування сітки: кнопки дій по 2 в ряд, кнопка назад - знизу
    builder.adjust(2, 1)
    
    return builder.as_markup()