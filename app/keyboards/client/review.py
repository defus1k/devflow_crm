from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_review_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Клавіатура для оцінки якості послуги (зірки 1-5).
    """
    builder = InlineKeyboardBuilder()
    
    # Кнопки з рейтингом
    for star in range(1, 6):
        builder.button(
            text=f"{'⭐' * star}", 
            callback_data=f"review_rate_{order_id}_{star}"
        )
    
    # Кнопка скасування відгуку
    builder.button(text="❌ Не зараз", callback_data=f"client_order_view_{order_id}")
    
    # Налаштування сітки: зірки в один ряд, кнопка "Не зараз" знизу
    builder.adjust(5, 1)
    
    return builder.as_markup()