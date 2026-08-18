from .dashboard import get_manager_dashboard_kb
from .orders import get_manager_orders_kb
from .statistics import get_manager_stats_kb
from .salary import get_manager_salary_kb
from .profile import get_manager_profile_kb


def get_manager_kb():
    return get_manager_dashboard_kb()


__all__ = [
    "get_manager_dashboard_kb",
    "get_manager_orders_kb",
    "get_manager_stats_kb",
    "get_manager_salary_kb",
    "get_manager_profile_kb",
    "get_manager_kb",
]