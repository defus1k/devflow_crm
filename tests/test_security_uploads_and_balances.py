import pytest
from decimal import Decimal

from app.services.balance_service import calculate_balance_after_debit, validate_balance_change
from app.services.security_service import validate_uploaded_file


def test_validate_uploaded_file_blocks_dangerous_extensions_and_large_files():
    assert validate_uploaded_file("payload.exe", "application/x-msdownload", 2 * 1024 * 1024) is False
    assert validate_uploaded_file("report.pdf", "application/pdf", 4 * 1024 * 1024) is True
    assert validate_uploaded_file("notes.txt", "text/plain", 60 * 1024 * 1024) is False


def test_validate_balance_change_rejects_invalid_amounts():
    with pytest.raises(ValueError):
        validate_balance_change(Decimal("-5"))

    with pytest.raises(ValueError):
        validate_balance_change(Decimal("10000001"))

    assert validate_balance_change(Decimal("250.50")) == Decimal("250.50")


def test_calculate_balance_after_debit_never_goes_negative():
    assert calculate_balance_after_debit(Decimal("100.00"), Decimal("250.00")) == Decimal("0.00")
