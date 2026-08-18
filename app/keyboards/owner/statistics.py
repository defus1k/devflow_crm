from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_owner_statistics_kb() -> InlineKeyboardMarkup:
    """
    Клавіатура вибору типу бізнес-аналітики для власника.
    """
    builder = InlineKeyboardBuilder()
    
    # Вибір типу звітів
    builder.button(text="📈 Динаміка продажів (за місяць)", callback_data="owner_stats_sales")
    builder.button(text="👥 Ефективність персоналу (KPI)", callback_data="owner_stats_staff")
    builder.button(text="📦 Популярні послуги", callback_data="owner_stats_services")
    builder.button(text="🔄 Конверсія замовлень", callback_data="owner_stats_conversion")
    
    # Повернення
    builder.button(text="🔙 Назад до дашборду", callback_data="owner_dashboard")
    
    builder.adjust(1)
    
    return builder.as_markup()