from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_support_kb() -> InlineKeyboardMarkup:
    """
    Клавіатура для швидкого зв'язку з підтримкою.
    """
    builder = InlineKeyboardBuilder()
    
    # Створення тікета через бота
    builder.button(text="📩 Створити тікет підтримки", callback_data="support_create_ticket")
    
    # Альтернативний канал (наприклад, посилання на адміна)
    builder.button(text="👨‍💻 Написати оператору", url="https://t.me/your_support_username")
    
    # Навігація
    builder.button(text="🔙 Назад у меню", callback_data="main_menu")
    
    builder.adjust(1)
    
    return builder.as_markup()