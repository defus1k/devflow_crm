from aiogram import Router

# Імпортуємо роутер з вашого dashboard.py
from .dashboard import router as dashboard_router

# Створюємо роутер для адмінки, який шукає головний файл
router = Router()

# Підключаємо роутер дашборду
router.include_router(dashboard_router)