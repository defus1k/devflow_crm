from enum import IntEnum

class CommissionRates(float, IntEnum):
    """
    Розподіл фінансів при успішному закритті замовлення.
    """
    DEVELOPER = 0.50  # 50%
    MANAGER = 0.40    # 40%
    COMPANY = 0.10    # 10%

class TimeLimits(IntEnum):
    """
    Тайм-ліміти для системи моніторингу працівників (у годинах).
    """
    TIKTOK_CHECK_INTERVAL = 48  # Періодичність перевірки відео
    WARNING_THRESHOLD = 72      # Попередження через 72 години
    TERMINATION_THRESHOLD = 96  # Заявка на звільнення через 96 годин

class FileLimits(IntEnum):
    """
    Обмеження на завантаження файлів (у МБ).
    """
    MAX_FILE_SIZE = 50 
    MAX_PROJECT_FILES = 10

class Pagination(IntEnum):
    """
    Налаштування пагінації для виводу списків у боті.
    """
    ITEMS_PER_PAGE = 5

# Списки ролей для зручної перевірки прав доступу
EMPLOYEE_ROLES = ["manager", "developer"]
ADMIN_ROLES = ["admin", "owner"]

# Коди валют для платіжних систем
SUPPORTED_CURRENCIES = ["USD", "EUR", "UAH", "USDT"]