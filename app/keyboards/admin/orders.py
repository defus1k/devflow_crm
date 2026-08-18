from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_admin_orders_kb(order_id: int, status: str) -> InlineKeyboardMarkup:
    """
    Клавіатура адміна для керування конкретним замовленням.
    :param order_id: ID замовлення.
    :param status: Поточний статус замовлення.
    """
    builder = InlineKeyboardBuilder()
    
    # Інформація та контроль
    builder.button(text="📋 Деталі замовлення", callback_data=f"admin_order_view_{order_id}")
    builder.button(text="🔄 Перепризначити виконавця", callback_data=f"admin_order_reassign_{order_id}")
    
    # Керування статусом (наприклад, якщо треба примусово завершити або скасувати)
    builder.button(text="🛑 Скасувати замовлення", callback_data=f"admin_order_cancel_{order_id}")
    
    # Повернення
    builder.button(text="🔙 Назад до списку замовлень", callback_data="admin_orders_list")
    
    builder.adjust(1)
    
    return builder.as_markup()