from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_owner_settings_kb() -> InlineKeyboardMarkup:
    """
    Клавіатура глобальних системних налаштувань.
    """
    builder = InlineKeyboardBuilder()
    
    # Керування основними параметрами
    builder.button(text="⚙️ Змінити валюту / комісію", callback_data="owner_set_finance")
    builder.button(text="🔧 Робочий режим бота (Maintenance)", callback_data="owner_set_status")
    builder.button(text="💬 Редагувати вітальні повідомлення", callback_data="owner_set_greetings")
    builder.button(text="🔄 Інтеграції (платіжні системи)", callback_data="owner_set_integrations")
    
    # Керування доступом
    builder.button(text="🔑 Налаштування рівнів доступу", callback_data="owner_set_access")
    
    # Повернення
    builder.button(text="🔙 Назад до дашборду", callback_data="owner_dashboard")
    
    builder.adjust(1)
    
    return builder.as_markup()