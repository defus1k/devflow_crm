from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_faq_kb() -> InlineKeyboardMarkup:
    """
    Клавіатура для навігації по розділах FAQ.
    """
    builder = InlineKeyboardBuilder()
    
    # Кнопки з категоріями питань
    builder.button(text="💳 Як оплатити?", callback_data="faq_payment")
    builder.button(text="🚚 Терміни доставки", callback_data="faq_delivery")
    builder.button(text="🛠 Як працює сервіс?", callback_data="faq_how_it_works")
    builder.button(text="📞 Контакти", callback_data="faq_contacts")
    
    # Кнопка повернення в меню
    builder.button(text="🔙 Назад", callback_data="main_menu")
    
    # Розміщення: категорії по 1, кнопка назад окремо
    builder.adjust(1, 1, 1, 1, 1)
    
    return builder.as_markup()