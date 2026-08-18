from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_back_kb(callback_data: str = "main_menu") -> InlineKeyboardMarkup:
    """
    Універсальна клавіатура для повернення назад.
    
    :param callback_data: Значення callback, на яке має повернути бот.
                          За замовчуванням повертає в головне меню.
    """
    builder = InlineKeyboardBuilder()
    
    # Використовуємо стандартний символ повернення
    builder.button(
        text="🔙 Назад", 
        callback_data=callback_data
    )
    
    return builder.as_markup()