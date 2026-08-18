from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_owner_finance_kb(balance: float, pending_payouts: float) -> InlineKeyboardMarkup:
    """
    Фінансовий дашборд власника.
    :param balance: Загальний баланс системи.
    :param pending_payouts: Сума, що очікує підтвердження виплати виконавцям.
    """
    builder = InlineKeyboardBuilder()
    
    # Головні фінансові показники
    builder.button(text=f"📊 Баланс: {balance:.2f} грн", callback_data="owner_fin_total")
    builder.button(text=f"💸 Очікують виплат: {pending_payouts:.2f} грн", callback_data="owner_fin_pending")
    
    # Інструменти управління
    builder.button(text="✅ Підтвердити виплати", callback_data="owner_fin_approve_payouts")
    builder.button(text="🧾 Історія транзакцій", callback_data="owner_fin_history")
    builder.button(text="📈 Звіт за період", callback_data="owner_fin_report")
    
    # Повернення
    builder.button(text="🔙 Назад до дашборду", callback_data="owner_dashboard")
    
    builder.adjust(1, 1, 1, 1, 1, 1)
    
    return builder.as_markup()