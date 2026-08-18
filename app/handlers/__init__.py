from aiogram import Dispatcher
from .admin import router as admin_router
from .common import router as common_router
from .client import router as client_router
from .manager import router as manager_router
from .developer import router as developer_router
from .owner import router as owner_router
from .balance import router as balance_router
def setup_routers(dp: Dispatcher):
    dp.include_router(common_router)
    dp.include_router(client_router)
    dp.include_router(manager_router)
    dp.include_router(developer_router)
    dp.include_router(admin_router)
    dp.include_router(owner_router)
    dp.include_router(balance_router)