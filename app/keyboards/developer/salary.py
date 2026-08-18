from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_performer_salary_kb(total_earned: float, pending_payout: float) -> InlineKeyboardMarkup:
    """
    Клавіатура фінансового звіту виконавця.
    :param total_earned: Всього зароблено за період.
    :param pending_payout: Сума, що очікує виплати.
    """
    builder = InlineKeyboardBuilder()
    
    # Інформаційні блоки
    builder.button(text=f"💰 Зароблено: {total_earned:.2f} грн", callback_data="performer_salary_total")
    builder.button(text=f"⏳ Очікує виплати: {pending_payout:.2f} грн", callback_data="performer_salary_pending")
    
    # Деталі та запити
    builder.button(text="🧾 Історія виплат", callback_data="performer_salary_history")
    builder.button(text="🏦 Замовити виплату", callback_data="performer_salary_request")
    
    # Повернення до дашборду виконавця
    builder.button(text="🔙 Назад до дашборду", callback_data="performer_dashboard")
    
    builder.adjust(1)
    
    return builder.as_markup()