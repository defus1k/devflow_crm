from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def get_developer_dashboard_kb(active_tasks: int = 0, error_count: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📥 Нові замовлення", callback_data="dev_available_orders")
    builder.button(text="👨‍💻 Мої проєкти", callback_data="dev_my_orders")
    builder.button(text="💬 Чат з менеджером", callback_data="dev_chats")
    builder.button(text="📂 Активні проєкти", callback_data="dev_active_projects")
    builder.button(text="🧾 Меню подання", callback_data="dev_submit_menu")
    builder.button(text="⏳ В роботі", callback_data="dev_in_progress")
    builder.button(text="🧪 На перевірці", callback_data="dev_under_review")
    builder.button(text="✅ Завершені", callback_data="dev_completed")
    builder.button(text="📁 Архів", callback_data="dev_archive")
    builder.button(text="🔍 Пошук замовлення", callback_data="dev_search")
    builder.button(text="💬 Чат з менеджером", callback_data="dev_chat_manager")
    builder.button(text="📎 Файли проєкту", callback_data="dev_files")
    builder.button(text="📝 Змінити статус", callback_data="dev_change_status")
    builder.button(text="📅 Дедлайни", callback_data="dev_deadlines")
    builder.button(text="🔔 Сповіщення", callback_data="dev_notifications")
    builder.button(text="📊 Моя статистика", callback_data="dev_statistics")
    builder.button(text="💸 Зарплата", callback_data="dev_salary")
    builder.button(text="⚙️ Налаштування", callback_data="dev_settings")
    builder.button(text="❓ Допомога", callback_data="dev_help")
    builder.adjust(2, 2, 2, 2, 2, 2, 2, 1)
    return builder.as_markup()