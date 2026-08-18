from aiogram import Router
from .dashboard import router as dashboard_router
from .orders import router as orders_router
from .users import router as users_router
from .blacklist import router as blacklist_router
from .broadcasts import router as broadcasts_router
from .logs import router as logs_router

router = Router()

router.include_router(dashboard_router)
router.include_router(orders_router)
router.include_router(users_router)
router.include_router(logs_router)
router.include_router(blacklist_router)
router.include_router(broadcasts_router)