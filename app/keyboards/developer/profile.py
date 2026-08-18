from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_performer_profile_kb(is_available: bool, specialization: str) -> InlineKeyboardMarkup:
    """
    Клавіатура профілю виконавця.
    :param is_available: Чи готовий виконавець брати нові задачі.
    :param specialization: Спеціалізація виконавця (наприклад, "Backend", "Frontend").
    """
    builder = InlineKeyboardBuilder()
    
    # Статус доступності
    status_text = "🟢 Доступний для задач" if is_available else "🔴 Зайнятий"
    builder.button(text=status_text, callback_data="performer_toggle_availability")
    
    # Інфо про компетенції
    builder.button(text=f"🛠 Спеціалізація: {specialization}", callback_data="performer_skills")
    
    # Налаштування сповіщень
    builder.button(text="🔔 Налаштування сповіщень", callback_data="performer_notif_settings")
    
    # Повернення
    builder.button(text="🔙 Назад до дашборду", callback_data="performer_dashboard")
    
    builder.adjust(1)
    
    return builder.as_markup()