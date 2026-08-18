from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def get_main_menu_kb(role: str = "client") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # ===== Клиент =====
    if role == "client":
        builder.button(
            text="📦 Сделать заказ",
            callback_data="create_order"
        )

        builder.button(
            text="📂 Мои заказы",
            callback_data="my_orders"
        )

        builder.button(
            text="⭐ Отзывы",
            callback_data="reviews"
        )

        builder.button(
            text="💼 Стать работником",
            callback_data="worker_application"
        )

        builder.button(
            text="👤 Личный кабинет",
            callback_data="profile"
        )

        builder.button(
            text="📞 Контакты",
            callback_data="contacts"
        )

    # ===== Рекламщик =====
    elif role == "manager":
        builder.button(
            text="📥 Очередь заказов",
            callback_data="manager_orders"
        )

        builder.button(
            text="📋 Мои проекты",
            callback_data="manager_my_orders"
        )

        builder.button(
            text="📊 KPI",
            callback_data="manager_kpi"
        )

        builder.button(
            text="💰 Баланс",
            callback_data="manager_balance"
        )

    # ===== Разработчик =====
    elif role == "developer":
        builder.button(
            text="� Взяти замовлення",
            callback_data="dev_available"
        )

        builder.button(
            text="💼 Мої проєкти",
            callback_data="dev_my_orders"
        )

        builder.button(
            text="📤 Здати роботу",
            callback_data="dev_submit_menu"
        )

        builder.button(
            text="💰 Статистика заробітку",
            callback_data="dev_salary"
        )

    # ===== Администратор =====
    elif role == "admin":
        builder.button(
            text="🛠 Панель администратора",
            callback_data="admin_panel"
        )

        builder.button(
            text="👥 Пользователи",
            callback_data="users"
        )

        builder.button(
            text="📦 Заказы",
            callback_data="orders"
        )

        builder.button(
            text="💰 Выплаты",
            callback_data="payments"
        )

    # ===== Владелец =====
    elif role == "owner":
        builder.button(
            text="👑 Owner Panel",
            callback_data="owner_panel"
        )

        builder.button(
            text="📈 Общая статистика",
            callback_data="global_stats"
        )

        builder.button(
            text="👥 Сотрудники",
            callback_data="employees"
        )

        builder.button(
            text="💵 Финансы",
            callback_data="finance"
        )

        builder.button(
            text="⚙ Настройки",
            callback_data="settings"
        )

    builder.adjust(1)

    return builder.as_markup()