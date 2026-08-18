from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_admin_tickets_kb(ticket_id: int) -> InlineKeyboardMarkup:
    """
    Клавіатура для обробки тікетів (звернень).
    :param ticket_id: ID звернення.
    """
    builder = InlineKeyboardBuilder()
    
    # Керування зверненням
    builder.button(text="✉️ Відповісти", callback_data=f"admin_ticket_reply_{ticket_id}")
    builder.button(text="✅ Закрити тікет", callback_data=f"admin_ticket_close_{ticket_id}")
    
    # Передача в інші відділи (наприклад, власнику, якщо питання фінансове)
    builder.button(text="➡️ Передати власнику", callback_data=f"admin_ticket_escalate_{ticket_id}")
    
    # Повернення
    builder.button(text="🔙 Назад до списку", callback_data="admin_tickets_list")
    
    builder.adjust(1)
    
    return builder.as_markup()