from aiogram import Router
from .dashboard import router as dashboard_router
from .employees import router as employees_router
from .finance import router as finance_router
from .payments import router as payments_router
from .role_switcher import router as role_switcher_router
from .role_switcher import router
# Додай сюди інші файли з папки owner, якщо вони в тебе є

router = Router()

# Об'єднуємо всі роутери папки в один
router.include_router(dashboard_router)
router.include_router(employees_router)
router.include_router(finance_router)
router.include_router(payments_router)
router.include_router(role_switcher_router)