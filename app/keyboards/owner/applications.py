from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_owner_applications_kb(app_id: int) -> InlineKeyboardMarkup:
    """
    Клавіатура для обробки нових вхідних заявок (на роботу або послуги).
    :param app_id: ID заявки для ідентифікації в базі.
    """
    builder = InlineKeyboardBuilder()
    
    # Рішення по заявці
    builder.button(text="✅ Прийняти", callback_data=f"app_accept_{app_id}")
    builder.button(text="❌ Відхилити", callback_data=f"app_reject_{app_id}")
    
    # Додаткові дії
    builder.button(text="👤 Переглянути профіль", callback_data=f"app_view_{app_id}")
    builder.button(text="💬 Зв'язатися", callback_data=f"app_contact_{app_id}")
    
    # Повернення
    builder.button(text="🔙 Назад до дашборду", callback_data="owner_dashboard")
    
    builder.adjust(2, 2, 1)
    
    return builder.as_markup()