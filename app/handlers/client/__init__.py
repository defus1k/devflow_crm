from aiogram import Router
from .menu import router as menu_router
from .create_order import router as create_order_router
from .profile import router as profile_router
from .support import router as support_router # ДОБАВЬТЕ ЭТОТ ИМПОРТ

router = Router()
# Включаем все роутеры в главный
router.include_routers(
    menu_router, 
    create_order_router, 
    profile_router,
    support_router # НЕ ЗАБУДЬТЕ ДОБАВИТЬ СЮДА
)