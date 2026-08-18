from types import SimpleNamespace

from app.keyboards.developer.dashboard import get_developer_dashboard_kb
from app.keyboards.manager.dashboard import get_manager_dashboard_kb
from app.handlers.manager.available_orders import _build_summary_text
from app.services.forum_service import (
    build_developer_offer_text,
    build_manager_accept_message,
    build_developer_accept_message,
)


def test_build_developer_offer_text_contains_required_fields():
    order = SimpleNamespace(
        id=42,
        title="CRM Bot",
        project_type="Telegram Bot",
        description="Need a CRM integration",
        budget=1500,
        contact="@client",
        created_at="2026-07-20 12:00:00",
        manager_id=1001,
        user_id=2002,
    )
    manager = SimpleNamespace(full_name="Alice", username="alice", telegram_id=1001)
    client = SimpleNamespace(full_name="Bob", username="bob", telegram_id=2002)

    text = build_developer_offer_text(order, manager, client)

    assert "ID заказа: 42" in text
    assert "Название проекта: CRM Bot" in text
    assert "Категория: Telegram Bot" in text
    assert "Описание: Need a CRM integration" in text
    assert "Стоимость: 1500" in text
    assert "Менеджер: Alice" in text
    assert "Клиент: Bob" in text
    assert "👀 Подробнее" in text
    assert "✅ Взять заказ" in text


def test_accept_messages_include_contact_hint_and_developer_data():
    manager = SimpleNamespace(full_name="Alice", username="alice", telegram_id=1001)
    developer = SimpleNamespace(full_name="Diana", username="diana", telegram_id=2002)

    manager_text = build_manager_accept_message(developer)
    developer_text = build_developer_accept_message(manager)

    assert "Вашу заявку на выполнение заказа принял разработчик" in manager_text
    assert "Diana" in manager_text
    assert "💬 Написать разработчику" in manager_text

    assert "Вы успешно приняли заказ" in developer_text
    assert "Alice" in developer_text
    assert "💬 Написать менеджеру" in developer_text


def test_manager_dashboard_contains_all_working_buttons():
    keyboard = get_manager_dashboard_kb()
    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert "manager_new_orders" in callbacks
    assert "manager_my_orders" in callbacks
    assert "manager_publish_order" in callbacks
    assert "manager_chats" in callbacks
    assert "manager_stats" in callbacks
    assert "manager_salary" in callbacks
    assert "manager_archive" in callbacks
    assert "manager_settings" in callbacks


def test_manager_order_summary_uses_ukrainian_template():
    data = {
        "platform": "Telegram",
        "project_name": "CRM Bot",
        "description": "Бот для CRM",
        "functions": "Модерація",
        "integrations": "PostgreSQL",
        "database": "Так",
        "admin_panel": "Так",
        "files_count": "2",
        "deadline": "20.08.2026",
        "budget": "12000",
        "wishes": "Нічого",
    }

    text = _build_summary_text(data)

    assert "📦 Нове замовлення" in text
    assert "📌 Назва проєкту" in text
    assert "📝 Додаткові побажання" in text
    assert "📅 Дедлайн" in text


def test_developer_dashboard_contains_all_working_buttons():
    keyboard = get_developer_dashboard_kb()
    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert "dev_my_orders" in callbacks
    assert "dev_available_orders" in callbacks
    assert "dev_chats" in callbacks
    assert "dev_active_projects" in callbacks
    assert "dev_submit_menu" in callbacks
    assert "dev_files" in callbacks
    assert "dev_deadlines" in callbacks
    assert "dev_statistics" in callbacks
    assert "dev_salary" in callbacks
    assert "dev_archive" in callbacks
    assert "dev_settings" in callbacks
