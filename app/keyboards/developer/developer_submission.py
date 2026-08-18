from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_developer_projects_kb(orders):
    builder = InlineKeyboardBuilder()
    for order in orders:
        builder.button(text=f"📦 #{order.id} - {order.title[:20]}", callback_data=f"submit_proj_{order.id}")
    builder.adjust(1)
    return builder.as_markup()

def get_owner_review_kb(order_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Прийняти", callback_data=f"owner_accept_{order_id}")
    builder.button(text="❌ Відправити на доопрацювання", callback_data=f"owner_reject_{order_id}")
    builder.adjust(1)
    return builder.as_markup()

def get_owner_client_transfer_kb(order_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="📤 Підтвердити відправку клієнту", callback_data=f"send_to_client_{order_id}")
    return builder.as_markup()