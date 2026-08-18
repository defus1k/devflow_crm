from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_confirm_kb(
    confirm_callback: str, 
    cancel_callback: str = "main_menu",
    confirm_text: str = "✅ Так",
    cancel_text: str = "❌ Ні"
) -> InlineKeyboardMarkup:
    """
    Клавіатура підтвердження дій.
    
    :param confirm_callback: callback для позитивного підтвердження.
    :param cancel_callback: callback для відміни (за замовчуванням повертає в головне меню).
    :param confirm_text: текст кнопки підтвердження.
    :param cancel_text: текст кнопки скасування.
    """
    builder = InlineKeyboardBuilder()
    
    builder.button(text=confirm_text, callback_data=confirm_callback)
    builder.button(text=cancel_text, callback_data=cancel_callback)
    
    # Розміщуємо кнопки в один рядок
    builder.adjust(2)
    
    return builder.as_markup()