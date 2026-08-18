from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Створити замовлення"), KeyboardButton(text="⭐ Відгуки")],
            [KeyboardButton(text="💼 Стати працівником"), KeyboardButton(text="👤 Особистий кабінет")],
            [KeyboardButton(text="📞 Контакти"), KeyboardButton(text="❓ Найчастіші питання")],
            [KeyboardButton(text="🛠 Послуги та підтримка")], # Додано сюди
        ],
        resize_keyboard=True,
        input_field_placeholder="Оберіть дію..."
    )

def get_project_type_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🤖 Telegram Bot"), KeyboardButton(text="🎮 Discord Bot")],
            
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )