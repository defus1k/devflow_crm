from aiogram.fsm.state import State, StatesGroup

class OrderStates(StatesGroup):
    """
    Машина станів (FSM) для створення замовлення.
    Дозволяє боту пам'ятати, на якому кроці зупинився користувач.
    """
    
    # Вибір типу послуги або назви
    waiting_for_title = State()
    
    # Введення опису завдання
    waiting_for_description = State()
    
    # Введення бюджету
    waiting_for_budget = State()
    
    # Завантаження посилання на ТЗ (технічне завдання)
    waiting_for_task_link = State()
    
    # Підтвердження та передплата
    waiting_for_confirmation = State()

class ManagerActionStates(StatesGroup):
    """
    Стани для менеджерів (прийняття/призначення замовлень).
    """
    waiting_for_manager_comment = State()
    waiting_for_developer_assignment = State()