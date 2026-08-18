from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram import Router
router = Router()

def get_admin_dashboard_kb(pending_applications: int, active_orders: int) -> InlineKeyboardMarkup:
    """
    Дашборд адміністратора.
    """
    builder = InlineKeyboardBuilder()
    
    # Оперативні індикатори
    builder.button(text=f"📥 Нові заявки: {pending_applications}", callback_data="admin_apps")
    builder.button(text=f"📦 Замовлення в роботі: {active_orders}", callback_data="admin_orders")
    
    # Інструменти управління
    builder.button(text="👥 Список користувачів", callback_data="admin_users_list")
    builder.button(text="� Модерація", callback_data="admin_users_list")
    builder.button(text="�📜 Логи", callback_data="admin_logs_menu")
    builder.button(text="👥 Список персоналу", callback_data="admin_staff_list")
    builder.button(text="🚨 Термінові питання", callback_data="admin_urgent_support")
    
    # Кнопка для адміна, щоб вийти в основне меню
    builder.button(text="🔙 До головного меню", callback_data="main_menu")
    
    # Коригуємо сітку: 1, 1, 1, 1, 2, 1
    builder.adjust(1, 1, 1, 1, 2, 1)
    
    return builder.as_markup()