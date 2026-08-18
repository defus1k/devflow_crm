from aiogram import Router
from .available_orders import router as available_orders_router
from .dashboard import router as dashboard_router
from .my_orders import router as my_orders_router
from .statistics import router as statistics_router
from .salary import router as salary_router
from .take_order import router as take_order_router
from .transfer_to_developer import router as transfer_to_developer_router
from .create_order import router as create_order_router 
# ДОДАЙТЕ ІМПОРТ НОВОГО ФАЙЛУ:


router = Router()
router.include_routers(
    available_orders_router,
    dashboard_router,
    my_orders_router,
    statistics_router,
    salary_router,
    take_order_router,
    transfer_to_developer_router,
    create_order_router,
    # ПІДКЛЮЧІТЬ РОУТЕР У СПИСОК:
    
)