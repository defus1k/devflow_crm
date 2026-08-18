from app.handlers.admin.users import build_user_moderation_text


def test_build_user_moderation_text_includes_status_and_history():
    user = type("User", (), {"full_name": "Alice", "telegram_id": 111, "username": "alice", "role": "client"})()
    moderation = type("Moderation", (), {"warnings": 2, "is_banned": True, "ban_reason": "spam"})()
    history = [
        {"action": "warn", "details": "Розсилка спаму", "created_at": "2024-01-01 10:00"},
        {"action": "ban", "details": "spam", "created_at": "2024-01-01 11:00"},
    ]

    text = build_user_moderation_text(user, moderation, history)

    assert "Alice" in text
    assert "Заблокований" in text
    assert "2" in text
    assert "warn" in text
    assert "ban" in text
