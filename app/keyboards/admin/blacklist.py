from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_admin_blacklist_kb(user_id: int) -> InlineKeyboardMarkup:
    """
    Клавіатура керування чорним списком.
    :param user_id: ID користувача, що знаходиться в списку.
    """
    builder = InlineKeyboardBuilder()
    
    # Керування статусом
    builder.button(text="🔓 Помилувати (розблокувати)", callback_data=f"admin_bl_unban_{user_id}")
    builder.button(text="📝 Додати примітку (причина бану)", callback_data=f"admin_bl_note_{user_id}")
    
    # Інформація
    builder.button(text="🔍 Переглянути історію порушень", callback_data=f"admin_bl_history_{user_id}")
    
    # Повернення
    builder.button(text="🔙 Назад до списку заблокованих", callback_data="admin_blacklist_list")
    
    builder.adjust(1)
    
    return builder.as_markup()