from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_manager_profile_kb(is_active: bool = True) -> InlineKeyboardMarkup:
    """
    Клавіатура профілю менеджера.
    :param is_active: Чи знаходиться менеджер на зміні (Ready/Offline).
    """
    builder = InlineKeyboardBuilder()
    
    # Статус роботи (на зміні або перерва)
    status_text = "🟢 На зміні (Приймати замовлення)" if is_active else "🔴 Поза зміною"
    builder.button(text=status_text, callback_data="manager_toggle_status")
    
    # Керування сповіщеннями
    builder.button(text="🔔 Налаштування сповіщень", callback_data="manager_settings_notif")
    
    # Доступ до даних
    builder.button(text="🆔 Мої права доступу", callback_data="manager_permissions")
    
    # Повернення до дашборду
    builder.button(text="🔙 Назад до дашборду", callback_data="manager_dashboard")
    
    builder.adjust(1)
    
    return builder.as_markup()