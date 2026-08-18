from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_start_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # Кнопка для початку реєстрації або переходу в меню
    builder.button(
        text="🚀 Розпочати роботу", 
        callback_data="start_work"
    )
    
    # Кнопка для отримання довідки
    builder.button(
        text="ℹ️ Допомога та FAQ", 
        callback_data="common_faq"
    )
    
    # Кнопка підтримки (якщо користувач зіткнувся з проблемою на старті)
    builder.button(
        text="🎧 Технічна підтримка", 
        callback_data="common_support"
    )
    
    # Налаштовуємо сітку: 1 кнопка у першому ряду, 2 у другому
    builder.adjust(1, 2)
    
    return builder.as_markup()