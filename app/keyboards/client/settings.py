from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_settings_kb(notifications_enabled: bool = True, language: str = "uk") -> InlineKeyboardMarkup:
    """
    Клавіатура налаштувань бота для клієнта.
    :param notifications_enabled: Стан сповіщень.
    :param language: Поточна мова інтерфейсу.
    """
    builder = InlineKeyboardBuilder()
    
    # Сповіщення
    notif_text = "🔕 Вимкнути сповіщення" if notifications_enabled else "🔔 Увімкнути сповіщення"
    builder.button(text=notif_text, callback_data="settings_toggle_notif")
    
    # Мова
    lang_text = f"🌐 Мова: {'🇺🇦 UA' if language == 'uk' else '🇬🇧 EN'}"
    builder.button(text=lang_text, callback_data="settings_toggle_lang")
    
    # Додаткові налаштування
    builder.button(text="🧹 Очистити кеш/дані", callback_data="settings_clear_cache")
    
    # Повернення
    builder.button(text="🔙 Назад у профіль", callback_data="client_profile")
    
    builder.adjust(1)
    
    return builder.as_markup()