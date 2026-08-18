from decimal import Decimal

MAX_BALANCE_AMOUNT = Decimal("10000000.00")


def validate_balance_change(amount: Decimal | float | int) -> Decimal:
    value = Decimal(str(amount))
    if value <= 0:
        raise ValueError("balance amount must be positive")
    if value > MAX_BALANCE_AMOUNT:
        raise ValueError("balance amount is too large")
    return value


def calculate_balance_after_debit(current_amount: Decimal | float | int, debit_amount: Decimal | float | int) -> Decimal:
    current = Decimal(str(current_amount))
    debit = Decimal(str(debit_amount))
    if debit <= 0:
        return current
    return max(Decimal("0.00"), current - debit)
