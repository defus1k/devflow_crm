from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_order_summary_kb(order_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # Кнопка підтвердження замовлення
    builder.button(text="✅ Підтвердити", callback_data="confirm_order")
    
    # Кнопка скасування, яка очищає стан та повертає в головне меню
    builder.button(text="❌ Скасувати", callback_data="cancel_order")
    
    builder.adjust(1) # Кнопки одна під одною
    return builder.as_markup()