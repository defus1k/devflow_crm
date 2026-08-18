from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_support_menu_kb() -> InlineKeyboardMarkup:
    """Головне меню розділу 'Послуги та підтримка'"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Пакети обслуговування", callback_data="support_packages")],
        [InlineKeyboardButton(text="➕ Додаткові послуги", callback_data="support_extra")],
        [InlineKeyboardButton(text="🚀 Замовити нову функцію", callback_data="support_new_feature")],
        [InlineKeyboardButton(text="📞 Зв'язатися з менеджером", callback_data="support_manager")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main_menu")]
    ])

def get_packages_kb() -> InlineKeyboardMarkup:
    """Меню вибору пакетів із кнопкою замовлення та повернення"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📞 Замовити пакет", callback_data="order_package_request")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_support_menu")]
    ])

def get_back_to_support_kb() -> InlineKeyboardMarkup:
    """Універсальна кнопка 'Назад' для підрозділів"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_support_menu")]
    ])