from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_manager_stats_kb() -> InlineKeyboardMarkup:
    """
    Клавіатура для вибору періоду перегляду статистики менеджера.
    """
    builder = InlineKeyboardBuilder()
    
    # Вибір періоду
    builder.button(text="📅 Сьогодні", callback_data="stats_period_today")
    builder.button(text="🗓 Тиждень", callback_data="stats_period_week")
    builder.button(text="📉 Цей місяць", callback_data="stats_period_month")
    
    # Додаткові звіти
    builder.button(text="⭐ Мій рейтинг (відгуки)", callback_data="stats_ratings")
    
    # Повернення до дашборду
    builder.button(text="🔙 Назад до дашборду", callback_data="manager_dashboard")
    
    builder.adjust(3, 1, 1)
    
    return builder.as_markup()