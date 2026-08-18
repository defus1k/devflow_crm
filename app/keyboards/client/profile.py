from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_profile_kb(is_premium: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="📝 Змінити ім'я", callback_data="profile_edit")
    builder.button(text="💸 Вивести кошти", callback_data="profile_withdraw") # Нова кнопка
    
    if is_premium:
        builder.button(text="⭐ Статус: Преміум", callback_data="profile_premium_info")
    else:
        builder.button(text="📊 Статистика замовлень", callback_data="profile_stats")
    
    builder.button(text="🔙 Назад у меню", callback_data="main_menu")
    builder.adjust(1)
    
    return builder.as_markup()