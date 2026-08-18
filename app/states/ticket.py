from aiogram.fsm.state import State, StatesGroup

class TicketStates(StatesGroup):
    """
    Машина станів для створення тікета в службу підтримки.
    """
    
    # Вибір теми або категорії проблеми
    waiting_for_title = State()
    
    # Детальний опис проблеми
    waiting_for_description = State()
    
    # Вибір рівня пріоритету (наприклад: Low, Medium, High, Urgent)
    waiting_for_priority = State()
    
    # Підтвердження створення та відправка
    waiting_for_confirmation = State()

class TicketReplyStates(StatesGroup):
    """
    Стани для адміністраторів (відповідь на тікет).
    """
    waiting_for_admin_response = State()