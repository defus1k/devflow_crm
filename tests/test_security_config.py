import pytest

from app.core.config import validate_settings_payload


def test_placeholder_secrets_rejected_in_production():
    payload = {
        "BOT_TOKEN": "your_bot_token_here",
        "OWNER_ID": 123456789,
        "CLIENT_FORUM_ID": -1000000000000,
        "MANAGER_FORUM_ID": -1000000000000,
        "DEVELOPER_FORUM_ID": -1000000000000,
        "REVIEWS_FORUM_ID": -1000000000000,
        "SUPPORT_FORUM_ID": -1000000000000,
        "FINANCE_FORUM_ID": -1000000000000,
        "DEVELOPER_ORDER_ID": -1000000000000,
        "DATABASE_URL": "postgresql+asyncpg://postgres:password@localhost:5432/devflow_crm",
        "JWT_SECRET": "change_me_in_production",
        "WEBHOOK_SECRET": "change_me_in_production",
        "ENVIRONMENT": "production",
    }

    with pytest.raises(ValueError):
        validate_settings_payload(payload, environment="production")
