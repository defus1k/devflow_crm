from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_kb(role: str = "client"):
    # Меню Owner
    if role == "owner":
        kb = [
            [KeyboardButton(text="👑 Панель власника"), KeyboardButton(text="⚙ Управління персоналом")],
            [KeyboardButton(text="📊 Глобальні звіти"), KeyboardButton(text="💳 Фінанси")],
            [KeyboardButton(text="📈 Операції"), KeyboardButton(text="📞 Контакти")]
        ]
    # Меню Admin
    elif role == "admin":
        kb = [
            [
                KeyboardButton(text="🛡 Панель адміна"),
                KeyboardButton(text="🛠 Модерація")
            ],
            [
                KeyboardButton(text="📋 Замовлення"),
                KeyboardButton(text="📜 Логи")
            ],
            [
                KeyboardButton(text="👤 Особистий кабінет"),
                KeyboardButton(text="❓ Найчастіші питання")
            ]
        ]
    # Меню Manager
    elif role == "manager":
        kb = [
            [KeyboardButton(text="💼 Панель менеджера"), KeyboardButton(text="📥 Передати замовлення в ІТ")],
            [KeyboardButton(text="📋 Активні замовлення"), KeyboardButton(text="👤 Особистий кабінет")],
            [KeyboardButton(text="📞 Контакти"), KeyboardButton(text="❓ Найчастіші питання")]
        ]
    elif role == "developer":
        kb = [
   
    [KeyboardButton(text="💼 Мої проєкти"), KeyboardButton(text="💬 Чат з менеджером")],
    [KeyboardButton(text="📊 Моя статистика"), KeyboardButton(text="👤 Особистий кабінет")],
    [KeyboardButton(text="📞 Підтримка"), KeyboardButton(text="❓ Допомога")]
]
    # Меню Client
    else:
        kb = [
            [KeyboardButton(text="🚀 Створити замовлення"), KeyboardButton(text="⭐ Відгуки")],
            [KeyboardButton(text="💼 Стати працівником"), KeyboardButton(text="👤 Особистий кабінет")],
            [KeyboardButton(text="❓ Найчастіші питання"), KeyboardButton(text="📞 Контакти")],  
            [KeyboardButton(text="🛠 Послуги та підтримка")]
        ]

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Оберіть дію...")