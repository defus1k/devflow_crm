from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_admin_users_kb(user_id: int, is_blocked: bool) -> InlineKeyboardMarkup:
    """
    Клавіатура для керування конкретним користувачем.
    :param user_id: ID користувача.
    :param is_blocked: Статус блокування.
    """
    builder = InlineKeyboardBuilder()
    
    # Керування статусом
    status_text = "🔓 Розблокувати" if is_blocked else "🚫 Заблокувати"
    builder.button(text=status_text, callback_data=f"admin_toggle_ban_{user_id}")
    
    # Інформаційні функції
    builder.button(text="ℹ️ Інфо про користувача", callback_data=f"admin_user_info_{user_id}")
    builder.button(text="💬 Надіслати повідомлення", callback_data=f"admin_user_msg_{user_id}")
    
    # Повернення
    builder.button(text="🔙 Назад до списку користувачів", callback_data="admin_users_list")
    
    builder.adjust(1)
    
    return builder.as_markup()