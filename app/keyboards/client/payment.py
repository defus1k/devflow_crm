from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_payment_kb(order_id: int, amount: int) -> InlineKeyboardMarkup:
    """Клавіатура рахунку"""
    builder = InlineKeyboardBuilder()
    builder.button(text=f"✅ Оплатити {amount} грн", callback_data=f"confirm_pay_{order_id}_{amount}")
    builder.button(text="🔙 Назад", callback_data=f"client_order_view_{order_id}")
    builder.adjust(1)
    return builder.as_markup()

def get_confirm_cancel_kb(order_id: int) -> InlineKeyboardMarkup:
    """Клавіатура підтвердження скасування замовлення"""
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Так, скасувати", callback_data=f"confirm_cancel_{order_id}")
    builder.button(text="🔙 Повернутися до оплати", callback_data=f"resume_pay_{order_id}")
    builder.adjust(1)
    return builder.as_markup()

def get_admin_payment_kb(user_id: int, order_id: int, amount: int) -> InlineKeyboardMarkup:
    """Клавіатура для адміністратора у форумі фінансів"""
    builder = InlineKeyboardBuilder()
    builder.button(text=f"✅ Зарахувати {amount} грн", callback_data=f"add_{user_id}_{order_id}_{amount}")
    builder.button(text="❌ Відхилити", callback_data=f"reject_{user_id}_{order_id}")
    builder.adjust(1)
    return builder.as_markup()