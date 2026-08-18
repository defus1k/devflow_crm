from aiogram.filters.callback_data import CallbackData


class DeveloperProjectCallback(CallbackData, prefix="dev_project"):
    action: str
    order_id: int
