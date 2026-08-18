from app.handlers.owner.finance import build_owner_finance_text


def test_build_owner_finance_text_includes_summary_and_payout_info():
    text = build_owner_finance_text(
        total_profit=1250.5,
        pending_orders=3,
        payments_pending=2,
        payments_success=5,
    )

    assert "Фінанси та виплати" in text
    assert "1250.50 грн" in text
    assert "3 замовлень" in text
    assert "2" in text and "5" in text
