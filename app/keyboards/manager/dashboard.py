from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_manager_dashboard_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🆕 Новые заявки", callback_data="manager_new_orders")
    builder.button(text="📦 Мои заказы", callback_data="manager_my_orders")
    builder.button(text="📢 Оставить заявку", callback_data="manager_publish_order")
    builder.button(text="💬 Чаты", callback_data="manager_chats")
    builder.button(text="📊 Моя статистика", callback_data="manager_stats")
    builder.button(text="💰 Мои заработки", callback_data="manager_salary")
    builder.button(text="🗂 Архив", callback_data="manager_archive")
    builder.button(text="⚙ Настройки", callback_data="manager_settings")
    builder.adjust(2)
    return builder.as_markup()