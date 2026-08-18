# keyboards/owner/__init__.py

from .dashboard import get_owner_dashboard_kb
#from .staff_management import get_staff_management_kb
#from .financial_reports import get_finance_kb
#from .system_settings import get_system_settings_kb

__all__ = [
    "get_owner_dashboard_kb",
    "get_staff_management_kb",
    "get_finance_kb",
    "get_system_settings_kb",
]