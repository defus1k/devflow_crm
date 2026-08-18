from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
# Імпортуємо загальну пагінацію для зручності
from app.keyboards.common.pagination import get_pagination_kb

def get_my_orders_kb(orders: list, page: int, total_pages: int) -> InlineKeyboardMarkup:
    """
    Список замовлень користувача з пагінацією.
    :param orders: Список словників [{'id': 101, 'status': 'Виконується'}, ...]
    """
    builder = InlineKeyboardBuilder()
    
    # Створюємо кнопки для кожного замовлення
    for order in orders:
        status_emoji = "⏳" if order['status'] == 'pending' else "✅"
        builder.button(
            text=f"{status_emoji} Замовлення #{order['id']}", 
            callback_data=f"client_order_view_{order['id']}"
        )
    
    builder.adjust(1) # Кожне замовлення в окремий рядок
    
    # Додаємо блок пагінації знизу
    pagination_kb = get_pagination_kb(page, total_pages, "client_orders")
    builder.attach(InlineKeyboardBuilder.from_markup(pagination_kb))
    
    # Кнопка повернення
    builder.button(text="🔙 Назад", callback_data="main_menu")
    builder.adjust(1)
    
    return builder.as_markup()