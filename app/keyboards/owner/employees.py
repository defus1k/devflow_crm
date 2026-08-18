from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_owner_employees_kb(employees: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for emp in employees:
        builder.button(
            text=f"{emp['name']} | {emp['role'].upper()}", 
            callback_data=f"owner_edit_emp_{emp['id']}"
        )
    
    builder.button(text="➕ Додати нового працівника", callback_data="owner_add_emp")
    builder.button(text="🔙 Назад до дашборду", callback_data="owner_dashboard")
    
    builder.adjust(1) # Всі кнопки списком
    return builder.as_markup()

def get_role_selection_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    roles = ["admin", "manager", "developer", "user"]
    
    for role in roles:
        builder.button(text=f"Надати роль: {role.upper()}", callback_data=f"set_role_{user_id}_{role}")
    
    builder.button(text="🔙 Скасувати", callback_data="owner_employees_list")
    builder.adjust(1)
    return builder.as_markup()