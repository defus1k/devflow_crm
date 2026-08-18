from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# =========================
# Вибір посади
# =========================

def get_position_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👨‍💼 Менеджер",
                    callback_data="position_manager"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👨‍💻 Python Developer",
                    callback_data="position_python"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Скасувати",
                    callback_data="cancel_application"
                )
            ]
        ]
    )


# =========================
# Після опису професії
# =========================

def get_continue_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Продовжити",
                    callback_data="application_continue"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="application_back"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Скасувати",
                    callback_data="cancel_application"
                )
            ]
        ]
    )


# =========================
# Підтвердження заявки
# =========================

def get_application_confirm_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подати заявку",
                    callback_data="submit_application"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Заповнити заново",
                    callback_data="restart_application"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Скасувати",
                    callback_data="cancel_application"
                )
            ]
        ]
    )


# =========================
# Для власника
# =========================

def get_owner_application_kb(application_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Прийняти",
                    callback_data=f"accept_application:{application_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Відхилити",
                    callback_data=f"reject_application:{application_id}"
                )
            ]
        ]
    )