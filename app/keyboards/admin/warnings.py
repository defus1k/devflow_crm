from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_admin_warnings_kb(user_id: int) -> InlineKeyboardMarkup:
    """
    Клавіатура для винесення офіційних попереджень користувачу.
    :param user_id: ID користувача, якому виноситься попередження.
    """
    builder = InlineKeyboardBuilder()
    
    # Типові причини попереджень
    builder.button(text="⚠️ Спам/реклама", callback_data=f"warn_spam_{user_id}")
    builder.button(text="⚠️ Неналежна поведінка", callback_data=f"warn_behavior_{user_id}")
    builder.button(text="⚠️ Порушення дедлайнів", callback_data=f"warn_deadline_{user_id}")
    builder.button(text="⚠️ Інше порушення", callback_data=f"warn_other_{user_id}")
    
    # Повернення
    builder.button(text="🔙 Назад до профілю користувача", callback_data=f"admin_user_info_{user_id}")
    
    builder.adjust(1)
    
    return builder.as_markup()