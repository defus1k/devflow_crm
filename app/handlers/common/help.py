from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """
    Виводить довідкову інформацію про можливості бота.
    """
    help_text = (
        "🛠 **Довідка Nexora BotForge**\n\n"
        "Я допоможу вам керувати вашими проєктами та комунікаціями.\n\n"
        "🔹 **Клієнтам:**\n"
        "• /create_order — Створити нове замовлення\n"
        "• /my_orders — Переглянути ваші угоди\n\n"
        "🔹 **Менеджерам/Розробникам:**\n"
        "• /dashboard — Ваша робоча панель\n"
        "• /statistics — Статистика виконання KPI\n\n"
        "🔹 **Контакти:**\n"
        "• /support — Зв'язатися з адміністрацією\n\n"
        "Якщо у вас виникли технічні проблеми, звертайтеся у підтримку через команду /support."
    )
    
    await message.answer(help_text, parse_mode="Markdown")