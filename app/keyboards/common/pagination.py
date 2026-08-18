from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_pagination_kb(
    page: int, 
    total_pages: int, 
    callback_prefix: str
) -> InlineKeyboardMarkup:
    """
    Генератор кнопок пагінації.
    
    :param page: Поточна сторінка (починається з 1).
    :param total_pages: Загальна кількість сторінок.
    :param callback_prefix: Префікс для кнопок (наприклад, 'client_orders').
    """
    builder = InlineKeyboardBuilder()
    
    buttons = []
    
    # Кнопка "Назад" (якщо не перша сторінка)
    if page > 1:
        buttons.append(
            {"text": "⬅️", "callback_data": f"{callback_prefix}_page_{page - 1}"}
        )
    
    # Кнопка з індикатором поточної сторінки
    buttons.append(
        {"text": f"{page} / {total_pages}", "callback_data": "ignore"}
    )
    
    # Кнопка "Вперед" (якщо не остання сторінка)
    if page < total_pages:
        buttons.append(
            {"text": "➡️", "callback_data": f"{callback_prefix}_page_{page + 1}"}
        )
    
    for btn in buttons:
        builder.button(text=btn["text"], callback_data=btn["callback_data"])
    
    builder.adjust(len(buttons))
    return builder.as_markup()