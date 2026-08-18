from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_owner_dashboard_kb(active_orders: int, total_profit: float, staff_online: int) -> InlineKeyboardMarkup:
    """
    Головна панель власника з основними бізнес-показниками.
    """
    builder = InlineKeyboardBuilder()
    
    # Ключові бізнес-метрики (неактивні кнопки як індикатори)
    builder.button(text=f"📦 Замовлень в роботі: {active_orders}", callback_data="owner_orders_report")
    builder.button(text=f"💰 Дохід: {total_profit:.2f} грн", callback_data="owner_finance_report")
    builder.button(text=f"👥 Команда онлайн: {staff_online}", callback_data="owner_staff_report")
    
    # Інструменти управління
    # Було:
# builder.button(text="⚙️ Керування персоналом", callback_data="owner_staff_manage")

# Стане (узгоджуємо з хендлером):
    builder.button(text="⚙️ Керування персоналом", callback_data="owner_employees_list")
    builder.button(text="📈 Фінанси та виплати", callback_data="owner_finance_manage")
    builder.button(text="🛠 Системні налаштування", callback_data="owner_settings")
    
    builder.adjust(1, 1, 1, 2, 1)
    
    return builder.as_markup()