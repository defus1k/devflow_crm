from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_admin_broadcast_kb() -> InlineKeyboardMarkup:
    """
    Клавіатура керування розсилками для адміністратора.
    """
    builder = InlineKeyboardBuilder()
    
    # Вибір цільової аудиторії
    builder.button(text="📢 Розсилка всім користувачам", callback_data="admin_bc_all")
    builder.button(text="👥 Розсилка активним виконавцям", callback_data="admin_bc_performers")
    builder.button(text="⚠️ Термінове сповіщення (технічне)", callback_data="admin_bc_urgent")
    
    # Інструменти
    builder.button(text="📝 Створити нове оголошення", callback_data="admin_bc_create")
    builder.button(text="🔙 Назад до дашборду", callback_data="admin_dashboard")
    
    builder.adjust(1)
    
    return builder.as_markup()