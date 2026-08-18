from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_performer_stats_kb(done_tasks: int, avg_hours: float, rating: float, total_earned: float) -> InlineKeyboardMarkup:
    """
    Клавіатура статистики, що динамічно відображає дані користувача.
    """
    builder = InlineKeyboardBuilder()
    
    # Виводимо реальні дані, які отримали з БД
    builder.button(text=f"✅ Задач: {done_tasks}", callback_data="performer_stats_total")
    builder.button(text=f"⏳ Ср. час: {avg_hours} год.", callback_data="performer_stats_time")
    builder.button(text=f"⭐ Рейтинг: {rating}/5.0", callback_data="performer_stats_rating")
    builder.button(text=f"💰 Дохід: {total_earned:.2f} грн", callback_data="performer_salary")
    
    # Повернення
    builder.button(text="🔙 Назад до списку задач", callback_data="performer_tasks")
    
    builder.adjust(2, 1, 1, 1)
    
    return builder.as_markup()