from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_briefing_kb(order_id: int, service_type: str) -> InlineKeyboardMarkup:
    """
    Клавіатура з інструкціями для конкретного типу замовлення.
    :param order_id: ID замовлення для повернення.
    :param service_type: Тип послуги для отримання інструкції.
    """
    builder = InlineKeyboardBuilder()
    
    # Кнопка отримання інструкції
    builder.button(
        text="📖 Чек-лист обробки", 
        callback_data=f"manager_brief_show_{service_type}"
    )
    
    # Швидка дія: почати виконання
    builder.button(
        text="🚀 Взяти в роботу", 
        callback_data=f"manager_order_take_{order_id}"
    )
    
    # Кнопка повернення до замовлення
    builder.button(
        text="🔙 До замовлення", 
        callback_data=f"manager_order_view_{order_id}"
    )
    
    builder.adjust(1)
    
    return builder.as_markup()