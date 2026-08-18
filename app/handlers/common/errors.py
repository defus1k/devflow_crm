import logging
import traceback

from aiogram import Router, types
from aiogram.types import ErrorEvent

router = Router()


@router.errors()
async def error_handler(event: ErrorEvent):
    """
    Глобальний обробник помилок.
    """

    logging.exception("Критична помилка")

    traceback.print_exception(
        type(event.exception),
        event.exception,
        event.exception.__traceback__,
    )

    if (
        isinstance(event.update, types.Update)
        and event.update.message
    ):
        await event.update.message.answer(
            "⚠️ Сталася внутрішня помилка.\n"
            "Адміністратор вже отримав інформацію про неї."
        )