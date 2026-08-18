from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_owner_broadcast_kb() -> InlineKeyboardMarkup:
    """
    Клавіатура для керування масовими розсилками.
    """
    builder = InlineKeyboardBuilder()
    
    # Вибір сегмента отримувачів
    builder.button(text="👤 Всім клієнтам", callback_data="owner_bc_all_clients")
    builder.button(text="👥 Тільки активним виконавцям", callback_data="owner_bc_performers")
    builder.button(text="📊 Сегмент: Останні замовники", callback_data="owner_bc_recent")
    
    # Інструменти управління
    builder.button(text="📝 Створити нове повідомлення", callback_data="owner_bc_create")
    builder.button(text="⏳ Черга розсилки", callback_data="owner_bc_queue")
    
    # Повернення
    builder.button(text="🔙 Назад до дашборду", callback_data="owner_dashboard")
    
    builder.adjust(1)
    
    return builder.as_markup()