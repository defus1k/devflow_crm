from aiogram import Router
from .dashboard import router as dashboard_router
from .available_orders import router as available_router
from .my_orders import router as my_orders_router
from .take_order import router as take_order_router
from .submission import router as submit_router
from .revisions import router as revisions_router
from .salary import router as salary_router
from .statistics import router as statistics_router
from .profile import router as profile_router

# Створюємо головний роутер для модуля розробника
router = Router()

# Реєструємо всі під-роутери
router.include_routers(
    dashboard_router,
    available_router,
    my_orders_router,
    take_order_router,
    submit_router,
    revisions_router,
    salary_router,
    statistics_router,
    profile_router,
)