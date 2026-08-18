from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_manager_salary_kb(current_balance: float) -> InlineKeyboardMarkup:
    """
    Клавіатура перегляду заробітної плати та бонусів.
    :param current_balance: Поточна сума заробітку.
    """
    builder = InlineKeyboardBuilder()
    
    # Інформація про баланс (неактивна кнопка як заголовок)
    builder.button(text=f"💰 Поточний баланс: {current_balance:.2f} грн", callback_data="ignore")
    
    # Дії з фінансами
    builder.button(text="📜 Історія нарахувань", callback_data="salary_history")
    builder.button(text="🎯 Бонусні цілі (KPI)", callback_data="salary_kpi_goals")
    
    # Повернення до дашборду
    builder.button(text="🔙 Назад до дашборду", callback_data="manager_dashboard")
    
    builder.adjust(1)
    
    return builder.as_markup()