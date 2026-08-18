from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def get_developer_order_tools_kb(order_id: int) -> InlineKeyboardMarkup:
    """Інструменти розробника для роботи з конкретним замовленням."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Скинути статус", callback_data=f"dev_order_reset_{order_id}")
    builder.button(text="🗑 Видалити запис", callback_data=f"dev_order_delete_{order_id}")
    builder.button(text="📝 Подивитися JSON", callback_data=f"dev_order_json_{order_id}")
    builder.button(text="🔙 Назад", callback_data="dev_my_orders")
    builder.adjust(1)
    return builder.as_markup()


def get_developer_project_actions_kb(order_id: int) -> InlineKeyboardMarkup:
    """Повноцінна панель дій для проекту розробника."""
    builder = InlineKeyboardBuilder()
    builder.button(text="📄 Переглянути опис", callback_data=f"dev_project_view_{order_id}")
    builder.button(text="💬 Написати менеджеру", callback_data=f"dev_project_message_{order_id}")
    builder.button(text="📎 Завантажити файл", callback_data=f"dev_project_upload_file_{order_id}")
    builder.button(text="📤 Завантажити результат", callback_data=f"dev_project_upload_result_{order_id}")
    builder.button(text="📝 Змінити статус", callback_data=f"dev_project_status_{order_id}")
    builder.button(text="⏱ Вказати прогрес (%)", callback_data=f"dev_project_progress_{order_id}")
    builder.button(text="📅 Змінити дедлайн", callback_data=f"dev_project_deadline_{order_id}")
    builder.button(text="📋 Переглянути історію", callback_data=f"dev_project_history_{order_id}")
    builder.button(text="⚠️ Повідомити про проблему", callback_data=f"dev_project_issue_{order_id}")
    builder.button(text="✅ Позначити як завершений", callback_data=f"dev_project_complete_{order_id}")
    builder.button(text="🔙 Назад", callback_data="dev_my_orders")
    builder.adjust(2, 2, 2, 2, 2, 1)
    return builder.as_markup()