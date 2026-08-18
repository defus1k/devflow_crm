from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from app.keyboards.common.pagination import get_pagination_kb

def get_manager_orders_kb(orders: list, page: int, total_pages: int, filter_type: str) -> InlineKeyboardMarkup:
    """
    Список замовлень для менеджера з фільтрами та пагінацією.
    :param orders: Список словників [{'id': 101, 'client_name': 'Олексій', 'status': 'new'}, ...]
    :param filter_type: Поточний фільтр (new, active, completed).
    """
    builder = InlineKeyboardBuilder()
    
    # Кнопки для кожного замовлення
    for order in orders:
        builder.button(
            text=f"№{order['id']} | {order['client_name']} | {order['status'].upper()}",
            callback_data=f"manager_order_view_{order['id']}"
        )
    
    builder.adjust(1)
    
    # Додаємо блок пагінації з нашої спільної бібліотеки
    pagination_kb = get_pagination_kb(page, total_pages, f"manager_orders_{filter_type}")
    builder.attach(InlineKeyboardBuilder.from_markup(pagination_kb))
    
    # Кнопка повернення до дашборду
    builder.button(text="🔙 Назад до дашборду", callback_data="manager_dashboard")
    builder.adjust(1)
    
    return builder.as_markup()