from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_owner_orders_kb() -> InlineKeyboardMarkup:
    """
    Інструменти власника для моніторингу та втручання в замовлення.
    """
    builder = InlineKeyboardBuilder()
    
    # Фільтрація для швидкого аудиту
    builder.button(text="🚨 Проблемні (завислі)", callback_data="owner_orders_stuck")
    builder.button(text="💰 Найвигідніші", callback_data="owner_orders_high_value")
    builder.button(text="🔍 Пошук за ID", callback_data="owner_orders_search")
    
    # Глобальні дії
    builder.button(text="📊 Звіт по замовленнях (CSV)", callback_data="owner_orders_export")
    
    # Повернення
    builder.button(text="🔙 Назад до дашборду", callback_data="owner_dashboard")
    
    builder.adjust(1)
    
    return builder.as_markup()