from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_admin_reviews_kb(review_id: int) -> InlineKeyboardMarkup:
    """
    Клавіатура для керування відгуками користувачів.
    :param review_id: ID відгуку для ідентифікації.
    """
    builder = InlineKeyboardBuilder()
    
    # Керування контентом відгуку
    builder.button(text="🔍 Деталі відгуку", callback_data=f"admin_rev_view_{review_id}")
    builder.button(text="🗑 Видалити відгук", callback_data=f"admin_rev_delete_{review_id}")
    
    # Зворотний зв'язок на відгук
    builder.button(text="💬 Відповісти від імені підтримки", callback_data=f"admin_rev_reply_{review_id}")
    
    # Повернення
    builder.button(text="🔙 Назад до списку відгуків", callback_data="admin_reviews_list")
    
    builder.adjust(1)
    
    return builder.as_markup()