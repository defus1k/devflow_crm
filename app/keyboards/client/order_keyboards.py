# app/keyboards/client/order_keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_project_type_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🤖 Telegram Bot"), KeyboardButton(text="🎮 Discord Bot")],
            
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )