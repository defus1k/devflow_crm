from aiogram import Router
from .start import router as start_router
from .help import router as help_router
from .faq import router as faq_router
from .reviews import router as reviews_router
from .support import router as support_router
from .contacts import router as contacts_router
from .worker_application import router as worker_application_router
from .errors import router as errors_router

# Створюємо роутер для модуля common
router = Router()

# Реєструємо всі під-роутери модуля
router.include_routers(
    start_router,
    help_router,
    faq_router,
    reviews_router,
    support_router,
    contacts_router,
    worker_application_router,
    errors_router
)