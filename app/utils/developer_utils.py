from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup


def safe_text(value: object | None, fallback: str = "—") -> str:
    return str(value) if value not in (None, "") else fallback


def format_project_summary(order: object) -> str:
    return (
        f"🛠 Проєкт #{getattr(order, 'id', 'n/a')}: {safe_text(getattr(order, 'title', None))}\n"
        f"Статус: {safe_text(getattr(order, 'status', None))}\n"
        f"Бюджет: {safe_text(getattr(order, 'budget', None), '0.00')}"
    )
