from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_cancel_kb(callback_data: str = "main_menu") -> InlineKeyboardMarkup:
    """
    Клавіатура для скасування поточного процесу (FSM).
    
    :param callback_data: Куди повернути користувача після скасування.
    """
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="❌ Скасувати дію", 
        callback_data=callback_data
    )
    
    return builder.as_markup()